import pdfplumber
# 提取文字太差
with pdfplumber.open("4.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
        print(text)
        if tables:
            print("***************************************************************************")
            for table in tables:
                print(table)
            print("***************************************************************************")
            