import tkinter as tk
from tkinter import messagebox
import random
import pygame

# -------------------------
# DOSYADAN SORU OKUMA
# -------------------------
import json

def sorulari_yukle(dosya_adi):
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            sorular = json.load(f)
            return sorular
    except:
        messagebox.showerror("Hata", "JSON dosyası okunamadı!")
        return []

# -------------------------
# SKOR KAYDET
# -------------------------
def skor_kaydet(isim, skor):
    with open("skorlar.txt", "a", encoding="utf-8") as f:
        f.write(f"{isim} - {skor} puan\n")

# -------------------------
# SORU SEÇ (EŞİT ZORLUK)
# -------------------------
def soru_sec(tum_sorular):
    kolay = [s for s in tum_sorular if s["zorluk"] == "kolay"]
    orta = [s for s in tum_sorular if s["zorluk"] == "orta"]
    zor = [s for s in tum_sorular if s["zorluk"] == "zor"]

    secilenler = []

    secilenler += random.sample(kolay, min(2, len(kolay)))
    secilenler += random.sample(orta, min(5, len(orta)))
    secilenler += random.sample(zor, min(3, len(zor)))

    random.shuffle(secilenler)
    return secilenler

# -------------------------
# GLOBAL
# -------------------------
index = 0
skor = 0
aktif_sorular = []
tum_sorular = sorulari_yukle("bilgi_yarismasi_quiz.json")
kullanici_adi = ""

# -------------------------
# OYUN BAŞLAT
# -------------------------
def oyunu_baslat():
    global aktif_sorular, index, skor, kullanici_adi

    kullanici_adi = isim_entry.get()

    if kullanici_adi.strip() == "":
        messagebox.showwarning("Uyarı", "İsim gir!")
        return

    if not tum_sorular:
        messagebox.showerror("Hata", "Soru yok!")
        return

    index = 0
    skor = 0
    aktif_sorular = soru_sec(tum_sorular)

    giris_frame.pack_forget()
    quiz_frame.pack()

    soru_goster()

# -------------------------
# SORU GÖSTER
# -------------------------
def soru_goster():
    global index

    if index >= len(aktif_sorular):
        sonucu_goster()
        return

    soru = aktif_sorular[index]
    soru_label.config(text=soru["soru"])

    for i, secenek in enumerate(soru["secenekler"]):
        butonlar[i].config(text=secenek)

# -------------------------
# CEVAP KONTROL
# -------------------------
def cevap_kontrol(secim):
    global index, skor

    soru = aktif_sorular[index]
    dogru = soru["dogru_cevap"]

    if secim == dogru:
        skor += 10
        dogru_ses.play()
        messagebox.showinfo("Sonuç", "Doğru!")
    else:
        yanlis_ses.play()
        messagebox.showerror("Sonuç", f"Yanlış! Doğru cevap: {dogru}")

    index += 1
    soru_goster()

# -------------------------
# SONUÇ
# -------------------------
def sonucu_goster():
    global kullanici_adi, skor

    try:
        with open("skorlar.json", "r", encoding="utf-8") as f:
            veriler = json.load(f)
    except:
        veriler = []

    veriler.append({"isim": kullanici_adi, "skor": skor})

    with open("skorlar.json", "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)

    quiz_frame.pack_forget()
    sonuc_label.config(text=f"{kullanici_adi}\nSkor: {skor}")
    sonuc_frame.pack()
# -------------------------
# TEKRAR
# -------------------------
def tekrar_baslat():
    sonuc_frame.pack_forget()
    giris_frame.pack()

# -------------------------
# GUI
# -------------------------
pygame.mixer.init()

dogru_ses = pygame.mixer.Sound("dogru.wav")
yanlis_ses = pygame.mixer.Sound("yanlis.wav")
root = tk.Tk()
root.title("Quiz Oyunu")
root.geometry("500x500")
root.configure(bg="#1E2A38")

# GİRİŞ
giris_frame = tk.Frame(root, bg="#1E2A38")
tk.Label(
    giris_frame,
    text="İsim Giriniz ",
    font=("Arial", 50, "bold"),
    bg="#03504C",
    fg="white"
).pack(padx=35 ,pady=35)
isim_entry = tk.Entry(giris_frame, font=("Arial", 25, "bold"))
isim_entry.pack(padx=25 ,pady=25)
tk.Button(giris_frame, text="Başla", font=("Arial", 25, "bold") ,command=oyunu_baslat).pack(padx=25 ,pady=25)
giris_frame.pack()
root.bind("<Return>", lambda event: oyunu_baslat())

# QUIZ
quiz_frame = tk.Frame(root, bg="#1E2A38")
soru_label = tk.Label(
    quiz_frame,
    text="",
    wraplength=500,
    font=("Arial", 30, "bold"),
    bg="#1E2A38",
    fg="white"
)
soru_label.pack(padx=25 ,pady=25)
  
# -------------------------
# HOVER EFEKTİ
# -------------------------
def hover(btn):
    btn["bg"] = "#E0BC92"

def leave(btn):
    btn["bg"] = "SystemButtonFace"
    
butonlar = []
for i in range(4):
    btn = tk.Button(quiz_frame, width=40, height=2, font=("Arial", 15, "bold"),
                    command=lambda i=i: cevap_kontrol(butonlar[i]["text"]))

    btn.pack(padx=15 ,pady=15)

    btn.bind("<Enter>", lambda e, b=btn: hover(b))
    btn.bind("<Leave>", lambda e, b=btn: leave(b))

    butonlar.append(btn)

# SONUÇ
sonuc_frame = tk.Frame(root, bg="#1E2A38")
sonuc_label = tk.Label(
    sonuc_frame,
    font=("Arial", 50),
    bg="#03504C",
    fg="white"
)
sonuc_label.pack(padx=35 ,pady=35)
tk.Button(sonuc_frame, text="Tekrar Oyna", command=tekrar_baslat, font=("Arial", 25, "bold")).pack(padx=25 ,pady=25)

root.mainloop()