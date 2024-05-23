from customtkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import random
import smtplib
import csv
import pandas as pd
from email.message import EmailMessage
from loginregist import register_user, login_user, menuDua

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("gui_tubes/purple.json") 

def halaman_login():
    window = ctk.CTk()
    window.title("login")
    window.geometry("800x400")
    window.resizable(False,False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image1_path = os.path.join(script_dir, "gambar/storyboard1.png")
    logo_path = os.path.join(script_dir, "gambar/logo_peti.png")

    img1 = Image.open(image1_path)
    img1 = ImageTk.PhotoImage(img1)

    logo_img = Image.open(logo_path)
    resize_img = logo_img.resize((100, 100))
    logo_img = ImageTk.PhotoImage(resize_img)

    l1 = ctk.CTkLabel(window, image=img1, text="")
    l1.pack()

    frame = ctk.CTkFrame(window, width=200, height=300, corner_radius=0, fg_color="White")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    l2 = ctk.CTkLabel(window, image=logo_img, text="", bg_color="white", fg_color="transparent")
    l2.place(relx=0.5, rely=0.21, anchor="center")

    l3 = ctk.CTkLabel(frame, text="Login", text_color="#1A1F23", font=('Trebuchet MS', 30))
    l3.place(relx=0.5, rely=0.26, anchor="center")

    entry_email = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Email", font=('Trebuchet MS',11), placeholder_text_color="#A6A4A8")
    entry_email.place(relx=0.5, rely=0.42, anchor="center")

    error_login = ctk.CTkLabel(frame, text="", text_color="red", font=('Trebuchet MS', 6))
    error_login.place(relx=0.59, rely=0.58, anchor="e")

    entry_password = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Password", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8", show="*")
    entry_password.place(relx=0.5, rely=0.52, anchor="center")

    def halaman_register():
        window.destroy()
        global window2
        window2 = ctk.CTk()
        window2.title("register")
        window2.geometry("800x400")
        window2.resizable(False,False)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image1_path = os.path.join(script_dir, "gambar/storyboard1.png")
        logo_path = os.path.join(script_dir, "gambar/logo_peti.png")

        img1 = Image.open(image1_path)
        img1 = ImageTk.PhotoImage(img1)

        logo_img = Image.open(logo_path)
        resize_img = logo_img.resize((100, 100))
        logo_img = ImageTk.PhotoImage(resize_img)

        l1 = ctk.CTkLabel(window2, image=img1, text="")
        l1.pack()

        frame = ctk.CTkFrame(window2, width=500, height=350, corner_radius=4, fg_color="White")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        l2 = ctk.CTkLabel(window2, image=logo_img, text="", bg_color="transparent", fg_color="transparent")
        l2.place(relx=0.5, rely=0.15, anchor="center")

        l3 = ctk.CTkLabel(frame, text="Register", text_color="#1A1F23", font=('Trebuchet MS', 30))
        l3.place(relx=0.5, rely=0.23, anchor="center")

        entry_nama_lengkap = ctk.CTkEntry(frame, width=400, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Nama Lengkap", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_nama_lengkap.place(relx=0.5, rely=0.33, anchor="center")

        entry_alamat = ctk.CTkEntry(frame, width=400, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Alamat", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_alamat.place(relx=0.5, rely=0.41, anchor="center")

        entry_nomor_hp = ctk.CTkEntry(frame, width=400, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="No. HP", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_nomor_hp.place(relx=0.5, rely=0.49, anchor="center")

        entry_username = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Username", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_username.place(relx=0.268, rely=0.6, anchor="center")

        entry_email = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Email", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_email.place(relx=0.268, rely=0.68, anchor="center")

        entry_password = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Password", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8", show="*")
        entry_password.place(relx=0.732, rely=0.6, anchor="center")

        error_pw_regis = ctk.CTkLabel(frame, text="", text_color="red", font=('Trebuchet MS', 6))
        error_pw_regis.place(relx=0.772, rely=0.725, anchor="e")

        entry_konfirmasi_password = ctk.CTkEntry(frame, width=170, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Konfirmasi Password", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8", show="*")
        entry_konfirmasi_password.place(relx=0.732, rely=0.68, anchor="center")

        def register_user():
            username = entry_username.get()
            email = entry_email.get()
            password1 = entry_password.get()
            password2 = entry_konfirmasi_password.get()
            namalengkap = entry_nama_lengkap.get()
            alamat = entry_alamat.get()
            nomorHP = entry_nomor_hp.get()
            
            if password1 != password2:
                error_pw_regis.configure(text="Password tidak sesuai. Coba lagi!")
                return
            
            otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
            send_otp(email, otp)

            window2.destroy()
            halaman_otp(email, otp, username, email, password1, namalengkap, alamat, nomorHP)

        button2 = ctk.CTkButton(frame, width=170, height=20, fg_color="transparent", border_width=0, text="Login", text_color="#A84F6C", font=("Trebuchet MS", 8), hover=False, command=back_login)
        button2.place(relx=0.55, rely=0.873, anchor="center")

        l4 = ctk.CTkLabel(frame, text="Sudah punya akun?", text_color="#1A1F23", font=('Trebuchet MS', 8))
        l4.place(relx=0.45, rely=0.87, anchor="center")

        button1 = ctk.CTkButton(frame, width=400, height=20, corner_radius=30, fg_color="#A84F6C", border_width=0, text="Daftar", text_color="White", font=("Trebuchet MS", 11), hover=True, hover_color="#66273B", command=register_user)
        button1.place(relx=0.5, rely=0.8, anchor="center")

        window2.mainloop()

    def halaman_otp(email, otp, username, user_email, password1, namalengkap, alamat, nomorHP):
        global window3
        window3 = ctk.CTk()
        window3.title("Verifikasi Kode OTP")
        window3.geometry("400x200")
        window3.resizable(False, False)

        frame = ctk.CTkFrame(window3, width=300, height=150, corner_radius=4, fg_color="White")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        l1 = ctk.CTkLabel(frame, text="Enter OTP", text_color="#1A1F23", font=('Trebuchet MS', 20))
        l1.place(relx=0.5, rely=0.2, anchor="center")

        entry_otp = ctk.CTkEntry(frame, width=200, height=20, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="OTP", font=('Trebuchet MS', 11), placeholder_text_color="#A6A4A8")
        entry_otp.place(relx=0.5, rely=0.5, anchor="center")

        error_otp = ctk.CTkLabel(frame, text="", text_color="red", font=('Trebuchet MS', 6))
        error_otp.place(relx=0.5, rely=0.7, anchor="center")

        def verify_otp():
            user_otp = entry_otp.get()
            if user_otp != otp:
                error_otp.configure(text="Kode OTP tidak sesuai. Coba lagi!")
            else:
                with open('gui_tubes/database/databaseUser.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, user_email, password1, namalengkap, alamat, nomorHP])
                
                window3.destroy()
                halaman_registration_successful()

        button_verify = ctk.CTkButton(frame, width=200, height=20, corner_radius=30, fg_color="#A84F6C", border_width=0, text="Verify OTP", text_color="White", font=("Trebuchet MS", 11), hover=True, hover_color="#66273B", command=verify_otp)
        button_verify.place(relx=0.5, rely=0.8, anchor="center")

        window3.mainloop()

    def halaman_registration_successful():
        global window4
        window4 = ctk.CTk()
        window4.title("")
        window4.geometry("400x200")
        window4.resizable(False, False)

        frame = ctk.CTkFrame(window4, width=300, height=150, corner_radius=4, fg_color="White")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        l1 = ctk.CTkLabel(frame, text="Registrasi berhasil!", text_color="#1A1F23", font=('Trebuchet MS', 20))
        l1.place(relx=0.5, rely=0.3, anchor="center")

        l2 = ctk.CTkLabel(frame, text="Kembali ke halaman login dalam beberapa detik.", text_color="#1A1F23", font=('Trebuchet MS', 11))
        l2.place(relx=0.5, rely=0.5, anchor="center")

        def redirect_to_login():
            window4.destroy()
            halaman_login()

        window4.after(3000, redirect_to_login)

        window4.mainloop()

    def send_otp(email, otp):
        msg = EmailMessage()
        msg['Subject'] = 'OTP Verification'
        msg['From'] = 'your-email@gmail.com'
        msg['To'] = email
        msg.set_content(f'Your OTP is {otp}')
    
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('your-email@gmail.com', 'your-email-password')
            smtp.send_message(msg)

    def back_login():
        window2.destroy()
        halaman_login()

    def login_user():
            email = entry_email.get()
            password = entry_password.get()
            
            # Membaca data pengguna dari file CSV
            with open('gui_tubes/database/databaseUser.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == email and row[2] == password:
                        window.destroy()  # Tutup halaman login
                        halaman_beranda(email)
                        return email  # Mengembalikan email pengguna saat login berhasil
            
            error_login.configure(text="Email atau password tidak sesuai")
            return None  # Mengembalikan None jika login gagal
            
    button1 = ctk.CTkButton(frame, width=170, height=20, corner_radius=30, fg_color="#A84F6C", border_width=0, text="Login", text_color="White", font=("Trebuchet MS", 11), hover=True, hover_color="#66273B",  command=login_user)
    button1.place(relx=0.5, rely=0.65, anchor="center")

    button2 = ctk.CTkButton(frame, width=170, height=20, fg_color="transparent", border_width=0, text="Daftar", text_color="#A84F6C", font=("Trebuchet MS", 8), hover=False, command=halaman_register)
    button2.place(relx=0.64, rely=0.753, anchor="center")

    l4 = ctk.CTkLabel(frame, text="Belum punya akun?", text_color="#1A1F23", font=('Trebuchet MS', 8))
    l4.place(relx=0.39, rely=0.75, anchor="center")

    window.mainloop()

def halaman_beranda(email):
    window_beranda = ctk.CTk()
    window_beranda.title("Beranda")
    window_beranda.geometry("1300x800")
    window_beranda.resizable(True,True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo2_path = os.path.join(script_dir, "gambar/logo2.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((384,216))
    logo2 = ImageTk.PhotoImage(resize_img)

    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
    l1.place(relx=0.2, rely=0, anchor="ne")


    

    window_beranda.mainloop()

if __name__ == "__main__":
    halaman_login()
