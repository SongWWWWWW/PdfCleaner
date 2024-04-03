import fitz # pyMuPDF里面的fitz包，不要与pip install fitz混淆
from rapidocr_onnxruntime import RapidOCR
import numpy as np
from typing import List
import tqdm
import re
RECOGNIZE_SENTENCE_LEN = 50
NUM_PERCENT = 0.6
"""
目标：将表格刚和图片的caption展示出来，其余内部相关内容都不要




表格的位置
1.正常段落之前
2.两个表格挨着
3.表格之后带着表格的描述内容

正常的表格形式
Table {num}: _______________________.



判断表格内容（优先级）：
1.表格后面是否还有表格
2.表格后是否有标题
3.表格后面是否有一行很长的字


new problems
1，表格的后面带着表格的描述内容，描述内容也被搞没了

"""
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
    file_path = './1.pdf'
    files = pdf_page_2text(file_path)
    text = ""
    for file in files:
        # print(file)
        text += file 
    find_matches(text)
    with open("log.txt","w") as f:
        for i in files:
            # print("-=-="*50)
            # print(repr(i))
            print(i)
            f.write(i)
        f.close()

# 第二步，把table标题之后的正文识别并跳过



