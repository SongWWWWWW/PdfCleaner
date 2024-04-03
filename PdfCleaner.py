import fitz # pyMuPDF里面的fitz包，不要与pip install fitz混淆
from rapidocr_onnxruntime import RapidOCR
import numpy as np
from typing import List,Tuple
import tqdm
import re
RECOGNIZE_SENTENCE_LEN = 50
NUM_PERCENT = 0.6
class PaperCleaner:
    def __init__(self,path: str) -> None:
        self.RECOGNIZE_SENTENCE_LEN = 50 #识别句子的长度
        self.paper_path = path # pdf的path
        self.NUM_PERCENT = 0.6 # 句子被认为是表格内容的数字比例
        self.text :List[str] = None # paper原文本内容
        self.cleaned_text: List[str]=None # 删除table内容后的文本内容
        self.read()
        self.clean_table_context()
    def read(self) -> None:
        """
        读取paper的内容，返回List[str]
        """
        doc = fitz.open(self.paper_path)
        self.text = [""]*doc.page_count
        self.cleaned_text = [""]*doc.page_count
        print(doc.page_count)
        b_unit = tqdm.tqdm(total=doc.page_count, desc="PaperPDFLoader context page index: 0")
        for i, page in enumerate(doc):
            b_unit.set_description("PaperPDFLoader context page index: {}".format(i))
            b_unit.refresh()
            text = page.get_text("")
            # 清除latex的公式内容
            cleaned_text = re.sub(r'<latexit[^>]*>(.*?)</latexit>', '', text, flags=re.DOTALL | re.IGNORECASE)
            self.text[i] = cleaned_text + "\n"
            # 识别表格内容并进行清除 pass
            b_unit.update(1)
        print(f"Paper path: {self.paper_path} has already been read")
    def find_matches(self) -> None:
        """
        调试函数，用来查看匹配的table
        """
        log_pattern = 0
        #  两种匹配模式
        # 第一种：Table 3: Experimental results on the DOTA dataset compared with state-of-the-art methods.
        # 第二种：Table 3. Experimental results on the DOTA dataset compared with state-of-the-art methods.
        pattern1 = r'Table (\d+): .+?(?=\.|\s*\n)'
        pattern2 = r'Table (\d+)\. .+?(?=\.|\s*\n)'
        print("="*100)
        for text in self.text:
            matches = list(re.finditer(pattern1, text))
            print(matches)
            if not matches:
                matches = re.finditer(pattern2, text)
                # print("pattern2 开始匹配")
            for match in matches:
                print(match.group())  # 打印匹配的文本
                print(match)
        print("="*100)
    def design_excel_content(self,text:str) -> bool:
        num = 0
        if not text:
            return False
        for i in text:
            if i>='0' or i<='9':
                num += 1
        if num/len(text) > NUM_PERCENT:
            return True
        return False
    def find_row_low_50_next(self,text:str) -> int:
        """
        text: 从0位置开始，找到小于长度50且数字多的行开始。

        """
        matches = re.finditer(r'\A.{0,49}\Z',text)
        for match in matches:
            if design_excel_content(text[match.start(),match.end()]):

                return match.start()
        return len(text)-1
    def find_row_over_50_next(self,text:str) -> int:

        """
        text: 从第一个小于50且数字多的行开始，找到第一个长度大于50的非数字行
        int：返回大于50的非数字行的首字母的位置
        
        """
        pos = find_row_low_50_next(text)
        for match in re.finditer(r'^(.{51,})\n', text[pos:], re.DOTALL):
            if not design_excel_content(match):
                if match.start() > 0:
                    return match.start()
        return len(text)-1
    def design_without_other_word(self,text:str) -> bool:
        """
        判断text之后在\n之前有无字符
        """
        for i in text:
            if i == ' ':
                continue
            elif i != '\n':
                return False
            elif i == '\n':
                return True
        return True
    def find_line_is_table_content(self,text:str)-> Tuple[int,int]:
        """
        找到table内容的开头和结尾+1
        开头是从第一个'\n'以后，找到'.'结尾的且长度小于50的或者之后小于50的句子
        结尾是超过50的行，且数字比例少
        """
        next_line_start = 0
        for index,character in enumerate(text):
            if character == "\n":
                next_line_start = index + 1
                break
        lines = text[next_line_start:].split("\n")
        table_position_start = next_line_start
        table_position_end = next_line_start
        transfer_travel = 0
        for index,line in enumerate(lines):
            if not transfer_travel:
                if len(line) < self.RECOGNIZE_SENTENCE_LEN:
                    if line:
                        if line[-1] == '.':
                            table_position_start += len(line)
                            table_position_end += len(line)
                            transfer_travel = 1
                            continue
                        elif lines[index-1][:-1] == '.':
                            transfer_travel = 1
                            table_position_end += len(line)
                            continue

                table_position_start += len(line)
                table_position_end += len(line)
            else:
                if len(line) > self.RECOGNIZE_SENTENCE_LEN and not design_excel_content(line):
                    break
                else:
                    table_position_end += len(line)
        return table_position_start,table_position_end        
    def cut_table_str(self,text:str,pos:int) -> str:
        """
        text: 需要切除table内容部分的text
        pos:text的table标题之后的第一个字符的位置
        
        """
        new_text = text
        table_start = 0
        table_end = 0
        if not self.design_without_other_word(text[pos:]): # 判断table这一行之后还有没有内容
            table_start,table_end = self.find_line_is_table_content(text[pos:]) # 将标题的内容隔过去
        else:
            # table_start = pos
            table_end = self.find_row_over_50_next(text[pos:])
            
        if self.design_excel_content(text[pos+table_start:pos+table_end]):
            return text[:pos+table_start] + text[pos+table_end:]
        else:
            print("\033[31m\033[1m error, 切除部分是非表格内容\033[0m\033[0m")
            print("-"*100)
            print(f"\033[34m{text[pos+table_start:table_end]}\033[0m")
            print("-"*100)
        return new_text 
    def recognize_table(self,text:str) ->str:

        """
        识别table的内容，并且切除table内部的内容
        """
        pattern1 = r'Table (\d+): .+?(?=\.|\s*\n)'
        pattern2 = r'Table (\d+)\. .+?(?=\.|\s*\n)'

        matches = list(re.finditer(pattern1, text))
        if not matches:
            matches = list(re.finditer(pattern2, text))
        if not matches:  
            return text
        else:
            index_first = [] # 匹配的标题的首个字母的text中的位置
            index_end = [] # 匹配的标题的最后的字母的之后第一个text中的位置
            new_text = ""
            for match in matches:
                index_first.append(match.start())
                index_end.append(match.end())
            index_first.append(len(text)-1) # 这里为了顺应后面的cut操作，通过添加一个元素，能够用index_first将text的分成若干个区间
            new_text += text[:index_first[0]] # 这里默认是table之后的内容是表格内容，之后会加入选择的情况
            for i in range(len(index_end)):
                new_text += self.cut_table_str(text[index_first[i]:index_first[i+1]],index_end[i]-index_first[i])
                # 上面将index_first分开的区间作为text传给cut函数，并将传入的text的table的长度传进去
            return new_text
    def clean_table_context(self) -> None:
        for index,text in enumerate(self.text):
            self.cleaned_text[index] = self.recognize_table(text)
        


def design_excel_content(text:str) -> bool:
    num = 0
    for i in text:
        if i>='0' or i<='9':
            num += 1
    if num/len(text) > NUM_PERCENT:
        return True
    return False
def find_row_low_50_next(text:str) -> int:
    """
    text: 从0位置开始，找到小于50且数字多的行开始。

    """
    matches = re.finditer(r'\A.{0,49}\Z',text)
    for match in matches:
        if design_excel_content(text[match.start(),match.end()]):
            return match.start()
    return len(text)-1
def find_row_over_50_next(text:str) -> int:

    """
    text: 从第一个小于50且数字多的行开始，找到第一个长度大于50的非数字行
    int：返回大于50的非数字行的首字母的位置
    
    """
    # print("`"*70)
    # print(text)
    # print("`"*70)
    # for match in re.finditer(r'(?!\n)(.{50,})(?!\n)', text, re.DOTALL):
    pos = find_row_low_50_next(text)
    for match in re.finditer(r'^(.{51,})\n', text[pos:], re.DOTALL):
        # 检查匹配的开始位置是否大于指定的开始位置
        # print(match.group(0))
        # print(match.start())
        # print(match.end())
        # print("`"*70)
        if not design_excel_content(match):
            if match.start() > 0:
                # print("match.start()",match.start())
                # 打印匹配的子字符串
                # print("找到长度大于50的子字符串:",text[match.start():match.end()])
                # 由于我们只需要找到第一个匹配，所以在这里我们可以停止搜索
                
                return match.start()
    return len(text)-1
def cut_middle_str(text:str,pos:int) -> str:
    """
    text: 需要切除table内容部分的text
    pos:text的table标题之后的第一个字符的位置
    
    """
    new_text = text
    middle = find_row_over_50_next(text[pos:])
    if design_excel_content(text[pos:pos+middle]):
        new_text = text[:pos] +"\n"+ text[pos + middle:]
    else:
        pass
    # print("*"*100)
    # print("cut_middle_str"+"-"*30)
    # print(text[pos:pos+middle])
    # print("*"*100)

    return new_text 
def recognize_table(text:str) ->str:

    """
    识别table的内容，并且切除table内部的内容
    """
    pattern1 = r'Table (\d+): .+?(?=\.|\s*\n)'
    pattern2 = r'Table (\d+)\. .+?(?=\.|\s*\n)'

    matches = list(re.finditer(pattern1, text))
    if not matches:
        matches = list(re.finditer(pattern2, text))
    if not matches:  
        return text
    else:
        index_first = []
        index_end = []
        new_text = ""
        for match in matches:
             index_first.append(match.start())
             index_end.append(match.end())
        index_first.append(len(text)-1)
        new_text += text[:index_first[0]]
        print("-=-=-=-=-=-==-=--=========-=-=-=-=--=-=--===--=")
        
        print("len(index_end):  ",len(index_end))
        print("-=-=-=-=-=-==-=--=========-=-=-=-=--=-=--===--=")
        for i in range(len(index_end)):
             new_text += cut_middle_str(text[index_first[i]:index_first[i+1]],index_end[i]-index_first[i])
        return new_text 
def pdf_page_2text(filepath) ->List[str]:
    """
    读取每页pdf，返回List[page.content]，用的是fitz（pyMuPDF）
    """
    # ocr = RapidOCR()
    doc = fitz.open(filepath)
    resp = [""]*doc.page_count
    print(doc.page_count)
    b_unit = tqdm.tqdm(total=doc.page_count, desc="RapidOCRPDFLoader context page index: 0")
    for i, page in enumerate(doc):
        b_unit.set_description("RapidOCRPDFLoader context page index: {}".format(i))
        b_unit.refresh()
        text = page.get_text("")
        # 清除latex的公式内容
        cleaned_text = re.sub(r'<latexit[^>]*>(.*?)</latexit>', '', text, flags=re.DOTALL | re.IGNORECASE)
        resp[i] = cleaned_text + "\n"

        # 识别表格内容并进行清除
        resp[i] = recognize_table(resp[i])
        b_unit.update(1)
    return resp
def find_matches(text:str) -> int:
    """
    调试函数，用来查看匹配的table
    """
    log_pattern = 0
    #  两种匹配模式
    # 第一种：Table 3: Experimental results on the DOTA dataset compared with state-of-the-art methods.
    # 第二种：Table 3. Experimental results on the DOTA dataset compared with state-of-the-art methods.
    pattern1 = r'Table (\d+): .+?(?=\.|\s*\n)'
    pattern2 = r'Table (\d+)\. .+?(?=\.|\s*\n)'

    matches = list(re.finditer(pattern1, text))
    print(matches)
    if not matches:
        matches = re.finditer(pattern2, text)
        print("kong")
        
    print("="*100)
    for match1 in matches:
        print(match1.group())  # 打印匹配的文本
        print(match1)
    print("="*100)
    return log_pattern 

        #  print(text[match.start():match.end()])
    print("="*100)
if __name__ == "__main__": 
    # file_path = './1.pdf'
    # files = pdf_page_2text(file_path)
    # text = ""
    # for file in files:
    #     # print(file)
    #     text += file 
    # find_matches(text)
    # with open("log.txt","w") as f:
    #     for i in files:
    #         # print("-=-="*50)
    #         # print(repr(i))
    #         print(i)
    #         f.write(i)
    #     f.close()
    files = PaperCleaner("./4.pdf")
    for text in files.cleaned_text:
        print(text)


# 对表格的内容清除还不到位
