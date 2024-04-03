import numpy as np
import pytesseract
from pdf2image import convert_from_path
import tqdm
# 不解析表格和图片
def pdf_ocr(fname, **kwargs):
	images = convert_from_path(fname, **kwargs)
	text = ''
	b_unit = tqdm.tqdm(total=len(images), desc="tesseract-ocr PDFLoader context page index: 0")
	for index,img in enumerate(images):
		b_unit.set_description("tesseract-ocr PDFLoader context page index: {}".format(index))
		b_unit.refresh()        
		img = np.array(img)
		text += pytesseract.image_to_string(img)
		b_unit.update(1)
	return text

fname = './4.pdf'
# text = pdf_ocr(fname, first_page=7, last_page=8)
text = pdf_ocr(fname)
print(text)
