import pytesseract
import cv2
#bir görüntüdeki dipnot benzeri küçük ve yatay bölümleri tespit etmeyi amaçlamaktadır.
def separate_footnotes():
    image = cv2.imread('data/sample_mgh.jpg')
    #image.shape: Görüntünün yüksekliği (im_h), genişliği (im_w) ve derinliğini (im_d) alır.
    im_h, im_w, im_d = image.shape
    base_image = image.copy()
    #cv2.cvtColor: Görüntüyü gri tonlamaya dönüştürür.
    # Gri tonlama, birçok görüntü işleme tekniği için daha uygun hale getirir.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.GaussianBlur: Gürültüyü azaltmak ve konturları daha belirgin hale getirmek için 7x7 Gauss bulanıklığı uygulanır.
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.threshold: Otsu yöntemi ile görüntüde ikili eşikleme yapılır.
    # Bu, görüntüyü siyah-beyaz hale getirerek nesneleri ve metinleri daha belirgin hale getirir
    #cv2.THRESH_BINARY_INV ise siyah ve beyaz bölgeleri tersine çevirir, metinler beyaz zemin üzerine siyah olur.
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #cv2.getStructuringElement: 50x10 boyutlarında dikdörtgen yapısal eleman oluşturur. Bu, dilatasyon işleminde kullanılan elemandır.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
    #cv2.dilate: Dilatasyon işlemi, beyaz olan alanların genişlemesine yol açar.
    # Bu, görüntüdeki metin ve dipnotların daha belirgin hale gelmesini sağlar.
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    #cv2.findContours: Dilatasyon uygulanmış görüntüdeki dış konturları bulur. Konturlar, nesnelerin sınırlarını temsil eder.
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #sorted: Tespit edilen konturlar, y eksenine göre yukarıdan aşağıya doğru sıralanır (dipnotların genelde sayfanın alt kısmında olduğunu varsayarak).
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
    for c in cnts:
        #cv2.boundingRect(c): Her kontur için bir dikdörtgen oluşturur ve bu dikdörtgenin koordinatlarını ve boyutlarını alır (x, y, w, h).
        x, y, w, h = cv2.boundingRect(c)
        #if h < 20 and w > 250: Yüksekliği 20 pikselden küçük ve genişliği 250 pikselden büyük olan konturların dipnot olabileceği varsayımı ile seçilir.
        # Bu, genellikle yatay olarak uzun ve ince olan dipnotları ayırt etmeyi amaçlar.
        if h < 20 and w > 250:
            #roi = base_image[0:y + h, 0:x + im_w]: Bu koordinatlara sahip bölge, ROI (Region of Interest - İlgi Alanı) olarak tanımlanır.
            roi = base_image[0:y + h, 0:x + im_w]
            #cv2.rectangle: Tespit edilen dipnot bölgesine dikdörtgen çizer.
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    cv2.imwrite("temp/output.png", roi)