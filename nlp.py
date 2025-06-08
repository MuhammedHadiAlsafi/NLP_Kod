# -*- coding: utf-8 -*-
"""
Güncellenmiş Diyalog Normalizasyonu - Özetleme İçin Hazır Hale Getirilmiş
@editors: M. Hadi and Furkan + ChatGPT önerileriyle
"""
import tkinter as tk
from tkinter import ttk
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Gerekli nltk verileri (ilk çalıştırmada indirmeniz gerekebilir)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# Informal / argo kelimeler listesi
informal_words = {
    'tbh', 'idk', 'lol', 'omg', 'brb', 'btw', 'u', 'ur', 'gonna', 'wanna'
}

# Basit düzeltme sözlüğü (homonim hataları, informal düzeltmeler)
corrections = {
    'as': 'ass',   # tahmini düzeltme
    'cookys': 'cookies',
    'postits': 'post-its'
}

def clean_line(line):
    # 1. Küçük harfe çevir
    line = line.lower()

    # 2. Noktalama temizle
    line = line.translate(str.maketrans('', '', string.punctuation))

    # 3. Sayı ve özel karakterleri kaldır
    line = re.sub(r'[^a-zA-Z\s]', '', line)

    # 4. Fazla boşlukları kaldır
    line = re.sub(r'\s+', ' ', line).strip()

    # 5. Tokenize et
    kelimeler = nltk.word_tokenize(line)

    # 6. Stopword, informal ve düzeltme işlemleri
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    temiz_kelimeler = []
    for k in kelimeler:
        if k in informal_words or k in stop_words:
            continue
        kelime_duzeltildi = corrections.get(k, k)
        temiz_kelimeler.append(lemmatizer.lemmatize(kelime_duzeltildi))

    # 7. Satırı tekrar birleştir
    return ' '.join(temiz_kelimeler)

def normalize_metin(metin):
    # Satır satır işle
    satirlar = metin.strip().split('\n')
    temiz_satirlar = [clean_line(satir) for satir in satirlar if satir.strip()]
    return '\n'.join(temiz_satirlar)

# Temizleme butonu işlemi
def metni_ozetle():
    girilen_metin = giris_alani.get("1.0", tk.END).strip()
    temiz_metin = normalize_metin(girilen_metin)

    cikti_alani.config(state='normal')
    cikti_alani.delete("1.0", tk.END)
    cikti_alani.insert(tk.END, temiz_metin)
    cikti_alani.config(state='disabled')

# Ana pencere
pencere = tk.Tk()
pencere.title("Diyalog Ön İşleyici")
pencere.geometry("800x500")
pencere.columnconfigure(1, weight=1)
pencere.rowconfigure(0, weight=1)
pencere.rowconfigure(1, weight=1)

# Etiketler
ttk.Label(pencere, text="Giriş Metni (Diyalog):").grid(row=0, column=0, padx=10, pady=10, sticky='nw')
ttk.Label(pencere, text="Temizlenmiş Metin:").grid(row=1, column=0, padx=10, pady=10, sticky='nw')

# Giriş alanı
giris_alani = tk.Text(pencere, wrap='word')
giris_alani.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Çıkış alanı
cikti_alani = tk.Text(pencere, wrap='word', state='disabled')
cikti_alani.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

# Buton
ozetle_butonu = ttk.Button(pencere, text="Temizle ve Göster", command=metni_ozetle)
ozetle_butonu.grid(row=2, column=0, columnspan=2, pady=10)

# Alt satırın boşlukla da esnemesi için
pencere.rowconfigure(2, weight=0)

# Başlat
pencere.mainloop()
