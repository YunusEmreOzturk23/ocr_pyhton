def Process_İmage():
    import cv2
    from  matplotlib import pyplot as plt
    from  PIL import  Image
    import pytesseract
    from IPython.display import display
    import numpy as np
    image_file= "data/page_01.jpg"
    img=cv2.imread(image_file)
    #cv2.imshow("original image", img)
    #cv2.waitKey(0)
    #display(image_file) #jupiter
    inverted_image =cv2.bitwise_not(img)#beyaz alanlar siyah siyah alanlar beyaz olur
    cv2.imwrite("temp/inverted.jpg",inverted_image)
    display("temp/inverted.jpg")
    #RESCALİNG
    #---------
    #Binarization
    def grayscale(image):#gri tonlamaya çevrilir
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray_image=grayscale(img)
    cv2.imwrite("temp/gray.jpg",gray_image)
    display("temp/gray.jpg")
    #İkili eşikleme işlemi ile gri tonlu görüntü, belirli bir eşik değerine göre siyah-beyaz hale getiriliyor.
    thresh, im_bw =cv2.threshold(gray_image,200,230,cv2.THRESH_BINARY)
    cv2.imwrite("temp/bw_image.jpg",im_bw)
    #------
    #noise_removal fonksiyonu, görüntüdeki gürültüyü gidermek için morfolojik işlemler uyguluyor.
    #Noise Removal
    def noise_removal(image):
        kernal = np.ones((1,1),np.uint8)
        #dilatasyon(büyütme)
        image = cv2.dilate(image,kernal, iterations=1)
        kernel = np.ones((1,1),np.uint8)
        #erozyon (küçültme)
        image=cv2.erode(image,kernel,iterations=1)
        #morphologyEx kullanılarak gürültüler gideriliyor
        image= cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
        #medianBlur ile yumuşatma işlemi yapılıyor.
        image=cv2.medianBlur(image,3)
        return (image)
    no_noise = noise_removal(im_bw)
    cv2.imwrite("temp/no_noise.jpg",no_noise)
    #Dilation And Erosion
    #thin_font fonksiyonu, görüntüdeki metinleri inceltmek için erozyon (erozyon) işlemi uyguluyor.
    def thin_font(image):
        image=cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8)
        image=cv2.erode(image,kernel,iterations=1)
        image=cv2.bitwise_not(image)
        return (image)
    eroded_image=thin_font(no_noise)
    cv2.imwrite("temp/eroded_image.jpg",eroded_image)
    #thick_font fonksiyonu, görüntüdeki metinleri kalınlaştırmak için dilatasyon işlemi uyguluyor.
    def thick_font(image):
        image=cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8)
        image=cv2.dilate(image,kernel,iterations=1)
        image=cv2.bitwise_not(image)
        return (image)
    dilated_image=thick_font(no_noise)
    cv2.imwrite("Temp/dilated_image.jpg",dilated_image)
    #Rotation/Deskewing
    new=cv2.imread("data/page_01_rotated.JPG")
    import numpy as np
    #getSkewAngle fonksiyonu, görüntünün eğik olup olmadığını bulmak için kullanılıyor.
    #Konturlar belirleniyor ve en büyük konturun eğim açısı hesaplanıyor.
    def getSkewAngle(cvImage) -> float:
        newImage = cvImage.copy()
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=2)
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours:
            rect = cv2.boundingRect(c)
            x, y, w, h = rect
            cv2.rectangle(newImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        largestContour = contours[0]
        print(len(contours))
        minAreaRect = cv2.minAreaRect(largestContour)
        cv2.imwrite("temp/boxes.jpg", newImage)
        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
        return -1.0 * angle

    # rotateImage fonksiyonu, görüntüyü verilen açıya göre döndürüyor.
    def rotateImage(cvImage, angle: float):
        newImage = cvImage.copy()
        newImage = cvImage.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage

    # deskew fonksiyonu, görüntüyü eğim açısını düzelterek döndürüyor.
    def deskew(cvImage):
        angle = getSkewAngle(cvImage)
        return rotateImage(cvImage, -1.0 * angle)

    fixed = deskew(new)
    cv2.imwrite("temp/rotated_fixed.jpg", fixed)
    display("temp/no_noise.jpg")
    #remove_borders fonksiyonu, görüntüdeki kenarlıkları kaldırıyor ve sadece ana içeriği (örneğin, metin veya belge kısmı) bırakıyor.

    def remove_borders(image):
        contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
        cnt = cntsSorted[-1]
        x, y, w, h = cv2.boundingRect(cnt)
        crop = image[y:y + h, x:x + w]
        return (crop)

    no_borders = remove_borders(no_noise)
    cv2.imwrite("temp/no_borders.jpg", no_borders)
    #copyMakeBorder fonksiyonu, görüntüye beyaz renkli (RGB değeri [255, 255, 255]) kenarlık ekliyor.
    color = [255, 255, 255]
    top, bottom, left, right = [150] * 4

    image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    cv2.imwrite("temp/image_with_border.jpg", image_with_border)