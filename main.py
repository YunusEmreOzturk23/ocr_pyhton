import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import re
from googletrans import Translator  # Çeviri için eklenen kütüphane

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
        self.root.geometry("800x800")

        # Dosya yükleme butonu
        self.label = tk.Label(root, text="Bir görüntü dosyası seçin:")
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Dosya Yükle", command=self.upload_file)
        self.upload_btn.pack()

        # Görüntüleme penceresi
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # OCR ve işleme butonları
        self.ocr_button = tk.Button(root, text="OCR (Tüm Metin)", command=self.run_ocr)
        self.ocr_button.pack(pady=5)

        self.bounding_box_button = tk.Button(root, text="Metin Kutuları Tespit Et", command=self.run_bounding_boxes)
        self.bounding_box_button.pack(pady=5)

        self.footnote_button = tk.Button(root, text="Dipnotları Ayır", command=self.run_footnotes)
        self.footnote_button.pack(pady=5)

        # Yeni Çeviri butonu
        self.translate_button = tk.Button(root, text="Çevir (İngilizce)", command=self.translate_text)
        self.translate_button.pack(pady=5)

        self.regex_label = tk.Label(root, text="Regex Deseni Girin:")
        self.regex_label.pack(pady=5)

        self.regex_entry = tk.Entry(root, width=50)
        self.regex_entry.pack(pady=5)

        self.regex_button = tk.Button(root, text="Regex ile Ara", command=self.run_regex)
        self.regex_button.pack(pady=5)

        # Metin kutusu
        self.text_area = tk.Text(root, wrap=tk.WORD, height=20)
        self.text_area.pack(pady=10, fill=tk.BOTH, expand=True)

        self.filepath = None

        # Regex desenleri
        self.patterns = {
            "VKN": r"VKN: (\d{10})",
            "Fatura No": r"Fatura No: (\w+)",
            "Fatura Tarihi": r"Fatura Tarihi: (\d{2}-\d{2}-\d{4})",
            "Fatura Saati": r"Fatura Saati: (\d{2}:\d{2}:\d{2})",
            "E-Posta": r"E-Posta: (\S+@\S+\.\S+)",
            "IBAN": r"IBAN\s+(\w{2}\d{2} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4} \d{2})",
            "Telefon": r"Tel: (\d{3}\d{8})",
            "Toplam Tutar": r"Vergiler Dahil Toplam Tutar\s+([0-9.,]+ TL)"
        }

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
            self.text_area.delete(1.0, tk.END)  # Önceki metni temizle
            self.text_area.insert(tk.END, ocr_result)  # OCR sonucunu ekle
            self.ocr_result = ocr_result  # Çeviri için OCR sonucunu sakla
            messagebox.showinfo("OCR Sonucu", "OCR işlemi tamamlandı!")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

    def translate_text(self):
        if hasattr(self, 'ocr_result') and self.ocr_result:  # OCR sonucu varsa
            translator = Translator()
            translated = translator.translate(self.ocr_result, src='tr', dest='en')
            self.text_area.delete(1.0, tk.END)  # Önceki metni temizle
            self.text_area.insert(tk.END, translated.text)  # Çeviriyi ekle
            messagebox.showinfo("Çeviri Sonucu", "Metin başarıyla İngilizce'ye çevrildi!")
        else:
            messagebox.showerror("Hata", "Lütfen önce OCR işlemi yapın!")

    def run_bounding_boxes(self):
        if self.filepath:
            results, entities = Bounding_Boxes(self.filepath)
            self.text_area.delete(1.0, tk.END)  # Önceki metni temizle
            self.text_area.insert(tk.END, "Bounding Boxes OCR Sonuçları:\n")
            self.text_area.insert(tk.END, "\n".join(results))
            self.text_area.insert(tk.END, "\n\nFiltrelenmiş Metinler:\n")
            self.text_area.insert(tk.END, "\n".join(entities))
            messagebox.showinfo("Tamamlandı", "Metin kutuları başarıyla tespit edildi.")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

    def run_footnotes(self):
        if self.filepath:
            separate_footnotes()
            messagebox.showinfo("Tamamlandı", "Dipnotlar başarıyla tespit edildi.")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

    def run_regex(self):
        if self.filepath:
            ocr_result = pytesseract.image_to_string(self.filepath)
            self.text_area.delete(1.0, tk.END)  # Önceki metni temizle

            # Regex desenleriyle arama yapma
            result_text = ""
            for label, pattern in self.patterns.items():
                match = re.search(pattern, ocr_result)
                if match:
                    result_text += f"{label}: {match.group(1)}\n"
                else:
                    result_text += f"{label}: bulunamadı.\n"

            self.text_area.insert(tk.END, result_text)
            messagebox.showinfo("Tamamlandı", "Regex işlemi tamamlandı!")
        else:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü yükleyin!")

# Uygulamayı çalıştırma
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApplication(root)
    root.mainloop()
