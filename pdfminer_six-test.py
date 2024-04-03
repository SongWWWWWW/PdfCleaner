from pdfminer.high_level import extract_text
# from pdfminer.layout import LAParams
# from pdfminer.high_level import extract_layout
text = extract_text('4.pdf')
print(text)



# with open('log.txt', 'w', encoding='utf-8') as f:
#     extract_layout(f, '4.pdf', laparams=LAParams(), pagenos=(0,))