import pytesseract
from PIL import Image
# import tesseract

img=Image.open('/home/maxtelll/Documents/oitavoSemestre/algoritmos/codigos/img.jpeg')
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

r=pytesseract.image_to_string(img)
print(r)