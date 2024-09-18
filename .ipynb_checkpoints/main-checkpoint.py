import cv2
from  matplotlib import pyplot as plt
from  PIL import  Image
import pytesseract
from IPython.display import display
image_file= "data/page_01.jpg"
img=cv2.imread(image_file)
#cv2.imshow("original image", img)
#cv2.waitKey(0)
#display(image_file) #jupiter
inverted_image =cv2.bitwise_not(img)
cv2.imwrite("temp/inverted.jpg",inverted_image)
display("temp/inverted.jpg")
#RESCALİNG



