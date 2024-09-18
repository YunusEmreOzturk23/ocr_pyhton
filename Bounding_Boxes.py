import pytesseract
import  cv2

def Bounding_Boxes():
    image= cv2.imread("data/index_02.JPG")
    base_image=image.copy()
    #cv2.cvtColor: Görüntüyü gri tonlamaya dönüştürür. OCR işlemleri için gri tonlama genellikle daha verimli olur.
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/index_gray.png",gray)
    #cv2.GaussianBlur: Görüntüyü 7x7 boyutundaki bir Gauss filtresi ile bulanıklaştırır. Bu işlem, gürültüyü azaltmak için yapılır.
    blur=cv2.GaussianBlur(gray,(7,7),0)
    cv2.imwrite("temp/index_blur.png",blur)
    #cv2.threshold: Otsu yöntemi kullanılarak bulanıklaştırılmış görüntüye ikili (binary) eşikleme uygulanır.
    # Bu, görüntüyü siyah-beyaz hale getirir ve metinlerin öne çıkmasını sağlar.
    thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    cv2.imwrite("temp/index_thresh.png",thresh)
    #cv2.getStructuringElement: 3x13 boyutunda dikdörtgen bir yapısal eleman oluşturur.
    #cv2.dilate: Eşiklenen görüntüde dilatasyon (genişletme) işlemi uygular, bu sayede konturlar daha belirgin hale gelir.
    kernal=cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
    cv2.imwrite("temp/index_kernel.png",kernal)
    dilate= cv2.dilate(thresh,kernal,iterations=1)
    cv2.imwrite("temp/index_dilate.png", dilate)
    #cv2.findContours: Dilatasyon işleminden sonra görüntüdeki konturları (nesne sınırları) tespit eder.
    cnts=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0] if len(cnts) == 2 else cnts[1]
    # sorted: Tespit edilen konturlar, x eksenine göre soldan sağa sıralanır.
    cnts=sorted(cnts,key=lambda  x:cv2.boundingRect(x)[0])
    results= []
    for c in cnts:
        #cv2.boundingRect: Her bir kontur için bir dikdörtgen çizilir ve koordinatları alınır.
        x,y,w,h=cv2.boundingRect(c)
        #if h>200 and w>20: Yüksekliği 200'den ve genişliği 20'den büyük olan konturların OCR işlemine alınmasını sağlar.
        # Bu, sadece büyük metin bloklarıyla çalışmak için yapılır.
        if h>200 and w>20:
            roi=image[y:y+h, x:x+h]
            cv2.imwrite("temp/index_roi.png", roi)
            cv2.rectangle(image, (x,y),(x+w, y+h),(36,255,12),2)
            #pytesseract.image_to_string(roi): Tesseract kullanarak, kontur içine alınan bölgedeki metin tanınır.
            ocr_result=pytesseract.image_to_string(roi)
            ocr_result=ocr_result.split("\n")
            for item in ocr_result:
                results.append(item)
    cv2.imwrite("temp/index_bbox.png", image)
    print(results)
    entities=[]
    for item in results:
        #strip(): Metindeki gereksiz boşluklar ve yeni satır karakterleri temizlenir.
        item=item.strip().replace("\n","")
        item=item.split(" ")[0]
        if len(item) >2:
            #if item[0] == "A": Metin "A" harfi ile başlıyorsa ve içinde "-" karakteri yoksa, metin filtrelenir.
            if  item[0]=="A" and "-" not in item:
                item=item.split(".")[0].replace(",","").replace(":","")
                entities.append(item)
    #print(entities)
    #list(set(entities)): Duplicates(tekrarlayan) elemanlar listeden çıkartılır.
    entities=list(set(entities))
    #print(entities)
    #entities.sort(): Filtrelenmiş metinler alfabetik olarak sıralanır ve ekrana yazdırılır.
    entities.sort()
    print(entities)