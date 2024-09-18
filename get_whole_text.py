import pytesseract
import cv2
#get_whole_text: Görüntüdeki tüm metinleri tanıyıp çıkartmak için oluşturulmuş fonksiyondur.
def get_whole_text():
    image= cv2.imread("data/sample_mgh.JPG")
    #base_image=image.copy(): Orijinal görüntünün bir kopyasını oluşturur, bu kopya üzerinde daha sonra OCR işlemi yapılacaktır.
    base_image=image.copy()
    #cv2.cvtColor: Görüntüyü gri tonlamaya dönüştürür. Gri tonlamalı görüntüler, OCR gibi işlemler için daha uygundur.
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #cv2.GaussianBlur: Görüntü, gürültüyü azaltmak için 7x7 boyutundaki bir Gauss filtresi ile bulanıklaştırılır.
    blur=cv2.GaussianBlur(gray,(7,7),0)
    #cv2.threshold: Otsu yöntemi ile ikili eşikleme yapılır. Bu işlem, görüntüyü siyah-beyaz yaparak metinlerin daha belirgin hale gelmesini sağlar.
    thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    #cv2.getStructuringElement: 3x50 boyutlarında dikdörtgen bir yapısal eleman oluşturur.
    kernal=cv2.getStructuringElement(cv2.MORPH_RECT,(3,50))
    #cv2.dilate: Dilatasyon işlemi, metin bloklarını genişleterek konturların daha net hale gelmesini sağlar.
    dilate=cv2.dilate(thresh,kernal,iterations=1)
    cv2.imwrite("temp/sample_dilated.png",dilate)
    #cv2.findContours: Dilatasyon uygulanmış görüntüdeki konturları (sınırları) bulur.
    cnts=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0] if len(cnts) == 2 else cnts[1]
    #sorted: Tespit edilen konturlar, y eksenine göre yukarıdan aşağıya doğru sıralanır (metinler satır satır işlenecek şekilde sıralanır).
    cnts=sorted(cnts, key=lambda x:cv2.boundingRect(x)[1])
    for c in cnts:
        #cv2.boundingRect: Her bir kontur için bir dikdörtgen çizer ve bu dikdörtgenin koordinatlarını alır.
        x,y,w,h=cv2.boundingRect(c)
        #if h > 200 and w > 250: Yüksekliği 200'den ve genişliği 250'den büyük olan konturlar,
        # ROI (Region of Interest) yani ilgi alanı olarak işlenir. Bu, yalnızca büyük metin bloklarının işlenmesi gerektiğini belirtir.
        if h >200 and w>250:
            roi= base_image[y:y+h,x:x+w]
            #cv2.rectangle: Görüntü üzerinde tespit edilen metin bölgelerine dikdörtgenler çizilir.
            cv2.rectangle(image,(x,y), (x+y,y+h),(36,255,12),2)
    cv2.imwrite("temp/sample_boxes.png",image)
    ocr_result_original =pytesseract.image_to_string(roi)
    print(ocr_result_original)
    #Özet:
    #Bu kod, verilen bir görüntüdeki metinleri tespit eder ve Tesseract OCR kullanarak tanımlar.
    # Görüntüdeki büyük metin blokları (belirli yükseklik ve genişlikteki) tespit edilip bunlara dikdörtgenler çizilir.
    # Ardından bu bölgelerdeki metinler okunur
    #ve ekrana yazdırılır. Bu işlem, büyük metin blokları olan belgelerde veya tablolar gibi yapılandırılmış görüntülerde işe yarar.