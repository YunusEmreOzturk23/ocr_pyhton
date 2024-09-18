import  pytesseract
from PIL import  Image

def ocr_index():
    image_file="data/index_02.JPG"
    img=Image.open(image_file)
    #pytesseract.image_to_string(img):
    # Tesseract OCR motoru kullanılarak, açılan görüntüdeki metinleri tespit eder ve metin olarak döner.
    # img, üzerinde OCR yapılacak görüntüdür.

    ocr_result=pytesseract.image_to_string(img)
    print(ocr_result)