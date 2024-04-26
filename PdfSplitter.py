import os
import sys
sys.path.append(os.path.dirname(__file__))
from pathlib import Path
import sys
import re
from PdfCleaner import PaperCleaner1 

class PaperSplitter(PaperCleaner1):
    def __init__(self, path: str = None, debug=None, clean=False) -> None:
        super().__init__(path,debug,clean)
        self.split_sign = ["Abstract","Introduction","Related Works","Methods","Conclusion"]
        self.texts = ""
        for i in self.text:
            self.texts += i + "\n"
    def splitter1(self):
        for i in self.split_sign:
            if i == "Abstract":
                s = rf"\b{i}\b"
            else:
                s = rf"\d+\.\s{i}"
            print(s)
            matches = re.findall(s,self.texts)
            for match in matches:
                print(match)
    def splitter2(self):
        for i in self.split_sign:
            if i == "Abstract":
                s = rf"\b{i}\b"
            else:
                s = rf"\d\n{i}"
                # s = rf"\d(\.\d)?\n{i}"
            print(s)
            matches = re.findall(s,self.texts,re.DOTALL)
            for match in matches:
                print(match)
    def splitter3(self):
            pattern = r'^\d+(\.\d+)+\s+[^\d\W]+.*'
            matches = re.findall(pattern,self.texts)
            for match in matches:
                print(match)
if __name__ == "__main__":
    splitter = PaperSplitter("./5.pdf")
    splitter.splitter3()
    # with open("log.txt","w") as f:
    #     for i in splitter.text:
    #         print(i)
    #         f.write(i)    
    # print("hello")
