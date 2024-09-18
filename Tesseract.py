import pytesseract
from PIL import Image
def Tesseract():
    img_file = "data/page_01.jpg"
    #Gürültüsü giderilmiş ve işlenmiş olan görüntü. OCR'nin daha doğru çalışabilmesi için bu işlenmiş görüntü üzerinde çalışıyoruz.
    no_noise = "temp/no_noise.jpg"
    img = Image.open(no_noise)
    #pytesseract.image_to_string(): Bu fonksiyon, belirtilen görüntüdeki metni tanır
    # bu metni düz bir yazı dizisi olarak döndürür.
    #Görüntü üzerinde yer alan yazıların metinsel karşılığı bu fonksiyonla elde edilir.
    #Girdi: Görüntü dosyası (burada no_noise olarak belirtilen dosya).
    #Çıktı: Görüntü üzerindeki yazının metin formatı (OCR sonucu).
    ocr_result = pytesseract.image_to_string(no_noise)
    print(ocr_result)
