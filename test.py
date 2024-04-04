text = """
Objective
IS
FID
˜µ prediction (baseline)
L, learned diagonal Σ
7.28±0.10
23.69
L, ﬁxed isotropic Σ
8.06±0.09
13.22
∥˜µ − ˜µθ∥2
–
–
ϵ prediction (ours)
L, learned diagonal Σ
–
–
L, ﬁxed isotropic Σ
7.67±0.13
13.51
∥˜ϵ − ϵθ∥2 (Lsimple)
9.46±0.11
3.17
"""
def is_num(c:str):
    if len(c) == 1:
        if c >= '0' and c <= '9':
            return True
    return False
num = 0
def design_excel_content(text:str) -> bool:
        num = 0
        if not text:
            return False
        for index,i in enumerate(text):
            if is_num(i):
                num += 1
            if i == "." :
                if index + 1 <= len(text) - 1:
                    if is_num(text[index-1]) and is_num(text[index+1]):
                        num += 2
                    else:
                        num += 1
            if i == '±' or i == "≤" or i == '≥': # 给权重
                num += 2
        num_line = 0
        chunk = text.split("\n")
        for k in chunk:
            if is_num_line(k):
                num_line += 1
        print(num/len(text))
        print(num_line/len(chunk))
        if num/len(text) >=  0.4 or num_line/len(chunk) >= 0.4:
            
            return True
        return False
def is_num_line(text:str):
    num = 0
    if not text:
        return False
    for i in text:
        if is_num(i) or i == '–'or i == '-' or i == '±' or i == '≤' or i == '≥' or i == '.':
            num += 1
    if num / len(text) >= 0.6:
        return True
    return False
print(design_excel_content(text))