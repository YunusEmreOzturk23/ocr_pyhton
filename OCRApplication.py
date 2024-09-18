import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract
from Process_İmage import Process_İmage
from Tesseract import Tesseract
from Bounding_Boxes import Bounding_Boxes
from ocr_index import ocr_index
from get_whole_text import get_whole_text
from separate_footnotes import separate_footnotes

class OCRApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Uygulaması")
        self.root.geometry("500x400")

        # Dosya yükleme butonu
        self.label = tk.Label(root, text="Bir görüntü dosyası seçin:")
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Dosya Yükle", command=self.upload_file)
        self.upload_btn.pack()

        # Görüntüleme penceresi
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # İşlem butonları
        self.ocr_button = tk.Button(root, text="OCR (Tüm Metin)", command=self.run_ocr)
        self.ocr_button.pack(pady=5)

        self.bounding_box_button = tk.Button(root, text="Metin Kutuları Tespit Et", command=self.run_bounding_boxes)
        self.bounding_box_button.pack(pady=5)

        self.footnote_button = tk.Button(root, text="Dipnotları Ayır", command=self.run_footnotes)
        self.footnote_button.pack(pady=5)

        self.filepath = None

    def upload_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.filepath:
            image = Image.open(self.filepath)
            image.thumbnail((300, 300))  # Görüntüyü uygun boyutlandır
            img = ImageTk.PhotoImage(image)
            self.image_label.config(image=img)
            self.image_label.image = img
            messagebox.showinfo("Başarılı", "Görüntü yüklendi!")
        else:
            messagebox.showerror("Hata", "Bir dosya seçilmedi!")

    def run_ocr(self):
        if self.filepath:
            ocr_result = pytesseract.image_to_string(self.filepath)
            print("OCR Sonucu:")
            print(ocr_result)
            messagebox.showinfo("OCR Sonucu", ocr_result)
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

    def run_bounding_boxes(self):
        if self.filepath:
            Bounding_Boxes()
            messagebox.showinfo("Tamamlandı", "Metin kutuları başarıyla tespit edildi.")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

    def run_footnotes(self):
        if self.filepath:
            separate_footnotes()
            messagebox.showinfo("Tamamlandı", "Dipnotlar başarıyla tespit edildi.")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

# Uygulamayı çalıştırma
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApplication(root)
    root.mainloop()