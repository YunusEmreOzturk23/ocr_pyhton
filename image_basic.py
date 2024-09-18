import cv2
from  PIL import  Image
import pytesseract
image_file= "data/page_01.jpg"
img=cv2.imread(image_file)
im= Image.open(image_file)
#print("İmage: ",im)
#print("Size: ",im.size)
#im.show(im)
#im.rotate(90).show()
im.save("temp/page_01.jpg")
