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

script_dir = os.path.dirname(os.path.abspath(__file__))
ctk.set_appearance_mode("dark")

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

        frame = ctk.CTkFrame(window2, width=500, height=350, corner_radius=0, fg_color="White")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        l2 = ctk.CTkLabel(window2, image=logo_img, text="", bg_color="white", fg_color="transparent")
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
                with open("database\databaseUser.csv", mode='a', newline='') as file:
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

    def send_otp(to_mail, otp):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        from_mail = "petibyunsofficial@gmail.com"
        server.login(from_mail, "johl erdn chfr jdgq")
        
        msg = EmailMessage()
        msg["Subject"] = "Your OTP Code for PETI"
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg.set_content("Hello, Your PETI OTP verification code is " + otp)
        
        server.send_message(msg)
        server.quit()
        print("Email sent")

    def back_login():
        window2.destroy()
        halaman_login()

    def login_user():
            email = entry_email.get()
            password = entry_password.get()
            
            # Membaca data pengguna dari file CSV
            with open('database/databaseUser.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == email and row[2] == password:
                        window.destroy()  # Tutup halaman login
                        setup_home_screen()
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
    def tampilkan_daftar_buku(scrollable_frame, file_path='database/databuku.csv'):
        try:
            # Membaca file CSV ke dalam DataFrame
            df = pd.read_csv(file_path, encoding="windows-1252")
            
            # Memeriksa apakah kolom 'judul' dan 'cover' ada dalam DataFrame
            if 'judul' not in df.columns or 'cover' not in df.columns:
                print("Kolom 'judul' atau 'cover' tidak ditemukan dalam file CSV.")
                return
            
            # Menampilkan daftar buku
            for idx, row in df.iterrows():
                cover_path = row['cover']
                
                if os.path.exists(cover_path):
                    try:
                        cover_image = Image.open(cover_path)
                        cover_image = cover_image.resize((300, 450))
                        cover_photo = ImageTk.PhotoImage(cover_image)
                    except Exception as e:
                        print(f"Error loading image {cover_path}: {e}")
                        cover_photo = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="red"))  # Tampilkan placeholder merah jika ada error
                else:
                    print(f"Cover image not found: {cover_path}")
                    cover_photo = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="gray"))  # Placeholder abu-abu jika gambar tidak ditemukan
                frame_buku = ctk.CTkFrame(scrollable_frame, width=360, height=600, fg_color="#1A1F23")
                frame_buku.pack(side="left", padx=10, pady=10)

            # Change label_cover to a button
                button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", command=lambda buku=row: tampilkan_detail_buku(buku))
                button_cover.image = cover_photo  # Menyimpan referensi gambar
                button_cover.pack(side="top")

                label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6", wraplength=300)
                label_judul.pack(side="top")
        
        except FileNotFoundError:
            print(f"File '{file_path}' tidak ditemukan.")
        except pd.errors.EmptyDataError:
            print(f"File '{file_path}' kosong atau tidak dapat dibaca.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

# Fungsi untuk menampilkan daftar buku berdasarkan genre yang dipilih
def tampilkan_buku_berdasarkan_genre(category_scrollable_frame, genre, file_path='database/databuku.csv'):
    try:
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Memeriksa apakah kolom 'judul' dan 'cover' ada dalam DataFrame
        if 'judul' not in df.columns or 'cover' not in df.columns:
            print("Kolom 'judul' atau 'cover' tidak ditemukan dalam file CSV.")
            return
        
        # Filter buku berdasarkan genre
        buku_genre = df[df['genre'].str.lower() == genre.lower()]
        
        if buku_genre.empty:
            print(f"Tidak ada buku dengan genre '{genre}' yang ditemukan.")
            return
        
        # Menghapus widget lama dari scrollable_frame
        for widget in category_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Menampilkan daftar buku berdasarkan genre
        for idx, row in buku_genre.iterrows():
            cover_path = row['cover']
            
            if os.path.exists(cover_path):
                try:
                    cover_image = Image.open(cover_path)
                    cover_image = cover_image.resize((300, 450))
                    cover_photo = ImageTk.PhotoImage(cover_image)
                except Exception as e:
                    print(f"Error loading image {cover_path}: {e}")
                    cover_photo = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="red"))  # Placeholder merah jika error
            else:
                print(f"Cover image not found: {cover_path}")
                cover_photo = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="gray"))  # Placeholder abu-abu jika tidak ditemukan

            frame_buku = ctk.CTkFrame(category_scrollable_frame, width=360, height=600, fg_color="#1A1F23")
            frame_buku.pack(side="left", padx=10, pady=10)

            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", command=lambda buku=row: tampilkan_detail_buku(buku))
            button_cover.image = cover_photo  # Menyimpan referensi gambar
            button_cover.pack(side="top")

            label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6", wraplength=300)
            label_judul.pack(side="top")
    
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print(f"File '{file_path}' kosong atau tidak dapat dibaca.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tampilkan_detail_buku(buku_dipilih):
  """Menampilkan detail buku dari kamus buku."""
  print(f"\n**Detail Buku:**")
  print(f"Judul: {buku_dipilih['judul']}")
  print(f"Genre: {buku_dipilih['genre']}")
  print(f"Penulis: {buku_dipilih['penulis']}")
  print(f"Tahun Terbit: {buku_dipilih['tahunTerbit']}")
  print(f"Halaman: {buku_dipilih['halaman']}")
  print(f"Sinopsis: {buku_dipilih['sinopsis']}")
  print(f"Stok: {buku_dipilih['stok']}")


def setup_home_screen():
    logo2_path = os.path.join(script_dir, "gambar/logo2.png")
    icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
    icon_acc_path = os.path.join(script_dir, "gambar/logout.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((320,117))
    logo2 = ImageTk.PhotoImage(resize_img)
    icon_search = Image.open(icon_search_path)
    resize_img = icon_search.resize((20,20))
    icon_search = ImageTk.PhotoImage(resize_img)
    icon_acc = Image.open(icon_acc_path)
    resize_img = icon_acc.resize((70,70))
    icon_acc = ImageTk.PhotoImage(resize_img)

    def search_button_click():
        judul_dicari = entry1.get().lower().strip()
        try:
            # Lakukan pencarian buku
            search_results = cari_buku(judul_dicari)
            # Tampilkan hasil pencarian
            show_result(search_results)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    
    def cari_buku(file_path='database/databuku.csv'):
        judul_dicari = entry1.get().lower().strip()
        try:
            # Membaca file CSV
            df = pd.read_csv(file_path, encoding="windows-1252")
            
            # Filter buku berdasarkan judul
            buku_ditemukan = df[df['judul'].str.lower().str.contains(judul_dicari)]
            
            if buku_ditemukan.empty:
                print(f"Tidak ada buku dengan judul yang mengandung '{judul_dicari}' ditemukan.")
            else:
                print(f"Buku yang ditemukan dengan judul yang mengandung '{judul_dicari}':")
                for index, row in buku_ditemukan.iterrows():
                    print(f"Judul: {row['judul']}, Penulis: {row['penulis']}, Tahun Terbit: {row['tahunTerbit']}, Halaman: {row['halaman']}")
                    print(f"Sinopsis: {row['sinopsis']}\n")
                    
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")


    def show_result(judul_dicari):
        search_results = cari_buku(judul_dicari)
        search_results_frame = ctk.CTkFrame(window_beranda, width=1200, height=700, fg_color="#1A1F23")
        search_results_frame.pack(pady=20)

        if search_results is not None and not search_results.empty:
            for idx, row in search_results.iterrows():
                book_image_path = os.path.join(script_dir, "cover buku", f"{row['judul']}.jpeg")
                book_description = row['sinopsis']
                show_book_details(search_results_frame, book_image_path, book_description)
                break
        else:
            no_result_label = ctk.CTkLabel(search_results_frame, text="Buku tidak ditemukan.", fg_color="transparent", text_color="#E3DFE6", font=("Trebuchet MS", 16))
            no_result_label.place(relx=0.5, rely=0.5, anchor="center")

    def indicate(label):
        button1_indicate.configure(fg_color="#1A1F23")
        button2_indicate.configure(fg_color="#1A1F23")
        # Highlight the selected indicator
        label.configure(fg_color="#A84F6C")
        
    def show_beranda():
        indicate(button1_indicate)
        category_frame.pack_forget()
        main_frame.pack(side=ctk.TOP, fill="both", expand=True)
        tampilkan_daftar_buku(scrollable_frame)

    def show_kategori():
        indicate(button2_indicate)
        main_frame.pack_forget()
        category_frame.pack(side=ctk.TOP, fill="both", expand=True)
        
        for widget in category_frame.winfo_children():
            widget.destroy()
        
        # Create the scrollable frame for displaying books
        global category_scrollable_frame
        category_scrollable_frame = ctk.CTkScrollableFrame(category_frame)
        category_scrollable_frame.pack(side=ctk.TOP, fill="both", expand=True)
        
        option_menu = ctk.CTkOptionMenu(
            category_frame, 
            values=["Novel", "Cerpen", "Biografi", "Komik", "Ensiklopedia", "Kamus", "Majalah"], 
            width=170, height=26, fg_color="#A6A4A8", 
            button_color="#A6A4A8", button_hover_color="#E3DFE6",
            text_color="#1A1F23", corner_radius=30, 
            command=lambda genre: tampilkan_buku_berdasarkan_genre(category_scrollable_frame, genre)
        )
        option_menu.place(relx=0.1, rely=0.02, anchor="n")

    # Fungsi untuk menampilkan frame akun
    def show_account_frame():
        acc_frame = ctk.CTkFrame(window_beranda, width=300, height=600, fg_color="#1A1F23", corner_radius=30, border_color="#A84F6C")
        acc_frame.pack(side=ctk.RIGHT, expand=False)
        acc_frame.pack_propagate(False)
        acc_frame.lift()

        label_acc_icon = ctk.CTkLabel(acc_frame, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", 
                        fg_color="#1A1F23", text="") 
        label_acc_icon.pack(pady=20)

        label_user = ctk.CTkLabel(acc_frame, text="dimas", fg_color="transparent", text_color="#E3DFE6", font=("Trebuchet MS", 18))
        label_user.pack(pady=20)

        # Menambahkan tombol "Buku Saya"
        button_buku_saya = ctk.CTkButton(acc_frame, text="Buku Saya", fg_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16), corner_radius=10)
        button_buku_saya.pack(pady=20)


    option_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    option_frame.pack(side=ctk.TOP)
    option_frame.pack_propagate(False)
    option_frame.configure(width=1300, height=120)

    main_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    main_frame.pack(side=ctk.TOP, fill="both", expand=True)
    main_frame.pack_propagate(False)
    main_frame.configure(width=1300, height=600) 

    category_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    category_frame.pack_forget()
    category_frame.pack_propagate(False)
    category_frame.configure(width=1300, height=600)

    search_results_mainframe = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    search_results_mainframe.pack_propagate(False)
    search_results_mainframe.configure(width=1300, height=600) 

    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
    l1.place(x=10, y=10, anchor="nw")

    entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", 
                       border_width=0, text_color="#1A1F23", placeholder_text="Search", 
                       font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
    entry1.place(relx=0.81, rely=0.055, anchor="center")

    button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_beranda)
    button1.place(relx=0.5, rely=0.055, anchor="center")

    button1_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", fg_color="#1A1F23")
    button1_indicate.place(relx=0.5, rely=0.4, anchor="center")

    button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_kategori)
    button2.place(relx=0.63, rely=0.055, anchor="center")

    button2_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", fg_color="#1A1F23")
    button2_indicate.place(relx=0.63, rely=0.4, anchor="center")

    button3 = ctk.CTkButton(window_beranda, width=20, height=20, image=icon_search, corner_radius=0, 
                        bg_color="#9C909D", fg_color="#9C909D", border_width=0, text="", 
                        hover=False, command=search_button_click)
    button3.place(relx=0.88, rely=0.055, anchor="center")

    button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", 
                            fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30", command=sys.exit)
    button4.place(relx=0.95, rely=0.055, anchor="center")

    scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=1200, height=500, fg_color="#1A1F23", orientation="horizontal")
    scrollable_frame.pack(side="top", fill="both", expand=True)

    search_results_frame = ctk.CTkFrame(search_results_mainframe, width=1300, height=600, fg_color="#1A1F23")
    scrollable_frame.pack(side="top", fill="both", expand=True)

    category_scrollable_frame = ctk.CTkScrollableFrame(category_frame, width=1200, height=500, fg_color="#1A1F23", orientation="vertical")
    category_scrollable_frame.pack(side="top", fill="both", expand=True)

    show_beranda()

    window_beranda = ctk.CTk()
    window_beranda.title("Beranda")
    window_beranda.geometry("1300x800")
    window_beranda.resizable(True,True)

    logo2_path = os.path.join(script_dir, "gambar/logo2.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((384,216))
    logo2 = ImageTk.PhotoImage(resize_img)

    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
    l1.place(relx=0.2, rely=0, anchor="ne")

    window_beranda.mainloop()

if __name__ == "__main__":
    halaman_login()
