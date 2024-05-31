from customtkinter import *
import customtkinter as ctk
from tkinter import Text
from PIL import Image, ImageTk
import os
import random
import smtplib
import csv
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pandas as pd
from email.message import EmailMessage
from loginregist import register_user, login_user, menuDua

ctk.set_appearance_mode("dark")

user_email = None
tanggal_pinjam = None
tanggal_kembali = None

def generate_random_code(length=10):
    """Menghasilkan kode random dari huruf dan angka."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_qr_code(data, filename):
    """Membuat dan menyimpan QR Code dari data yang diberikan."""
    img = qrcode.make(data)
    img.save(filename)

def read_user_data(email):
    """Membaca data pengguna dari databaseUser.csv berdasarkan email."""
    with open('database/databaseUser.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email:
                return row['namalengkap']
    return None

def read_book_cover(buku_dipilih):
    """Membaca path gambar cover buku dari databuku.csv berdasarkan judul buku."""
    with open('database/databuku.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['judul'] == buku_dipilih:
                return row['cover']
    return None

def save_loan_ticket_to_database(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali, pdf_filename):
    """Menyimpan informasi tiket peminjaman ke database datapinjam.csv."""
    fieldnames = ['email', 'judul', 'tanggalPinjam', 'tanggalKembali', 'tiket']

    # Debug print statement untuk memeriksa tipe dan isi dari buku_dipilih
    print("Tipe buku_dipilih:", type(buku_dipilih))
    print("Isi buku_dipilih:", buku_dipilih)

    # Ekstraksi judul buku jika buku_dipilih adalah DataFrame atau Series
    if isinstance(buku_dipilih, pd.Series):
        judul_buku = buku_dipilih['judul']
    elif isinstance(buku_dipilih, pd.DataFrame):
        judul_buku = buku_dipilih['judul'].iloc[0]
    else:
        judul_buku = buku_dipilih  # Jika bukan DataFrame atau Series, asumsikan ini adalah string judul langsung

    # Debug print statement untuk memeriksa judul_buku
    print("Judul Buku:", judul_buku)

    new_entry = {
        'email': user_email,
        'judul': judul_buku,
        'tanggalPinjam': tanggal_pinjam,
        'tanggalKembali': tanggal_kembali,
        'tiket': pdf_filename
    }

    # Debug print statement untuk memeriksa new_entry
    print("New Entry:", new_entry)

    # Membaca data dari file datapinjam.csv
    if not os.path.exists('database/datapinjam.csv'):
        # Jika file belum ada, buat file baru dengan header
        with open('database/datapinjam.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(new_entry)
    else:
        # Jika file sudah ada, tambahkan entri baru
        with open('database/datapinjam.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(new_entry)

def print_and_open_ticket(c):
    """Mencetak tiket peminjaman dan membuka tiket ke browser."""
    pdf_filename = f"tiket/tiket_peminjaman_{random_code}.pdf"  # Ubah sesuai dengan struktur penyimpanan Anda
    c.showPage()
    c.save()

    print(f"Tiket peminjaman telah disimpan sebagai {pdf_filename}")
    webbrowser.open_new(f"file://{os.path.abspath(pdf_filename)}")

    return pdf_filename

def create_loan_ticket(user_email, buku_dipilih, genre, penulis, tanggal_pinjam, tanggal_kembali):
    """Membuat tiket peminjaman buku dalam bentuk PDF dan menyimpannya ke database."""
    # Mendefinisikan jenis font dan ukuran font untuk teks
    font_styles = {
        "title": ("Times-Italic", 25),
        "normal": ("Helvetica", 17),
        "italic": ("Times-Italic", 17),
        "bold": ("Times-Bold", 12),
        "book": ("Times-Bold", 20),
        "bottom":("Times-Italic", 15)
    }

    # Membaca nama lengkap pengguna dari database
    nama_lengkap = read_user_data(user_email)
    if not nama_lengkap:
        print(f"Pengguna dengan email {user_email} tidak ditemukan.")
        return
    
    # Membaca path gambar cover buku dari database
    cover_path = read_book_cover(buku_dipilih)
    if not cover_path:
        print(f"Cover buku untuk {buku_dipilih} tidak ditemukan.")
        return
    
    # Menghasilkan kode random dan QR code
    random_code = generate_random_code()
    qr_filename = f"tiket/{random_code}.png"  
    generate_qr_code(random_code, qr_filename)
    
    # Membuat PDF dengan ukuran A5 landscape
    c = canvas.Canvas(pdf_filename, pagesize=landscape(A5))
    width, height = landscape(A5)

    # Mengatur warna latar belakang canvas menjadi hitam
    c.setFillColorRGB(0, 0, 0)
    c.rect(0, 0, width, height, fill=1)

    # Garis batas atas
    c.setStrokeColorRGB(0.5, 0.3, 0.1)
    c.setLineWidth(3)
    c.line(20, 295, 425, 295)
    # Garis batas bawah
    c.setStrokeColorRGB(0.5, 0.3, 0.1)
    c.setLineWidth(1.5)
    c.line(20, 125, 425, 125)

    # Menambahkan logo perusahaan ke PDF dan mengubah ukurannya
    logo_path = "gambar/logo2.png"
    logo_width = 300  # Ukuran lebar logo dalam pixel
    logo_height = 100  # Ukuran tinggi logo dalam pixel
    logo_x = 20  # Koordinat x untuk pojok kiri atas
    logo_y = height - logo_height - 20  # Koordinat y untuk pojok kiri atas
    c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)
    
    # Menambahkan teks ke PDF dengan jenis font, ukuran font, dan posisi yang berbeda
    title_font_name, title_font_size = font_styles["title"]
    title_text = "Tiket Peminjaman Buku"
    title_text_width = c.stringWidth(title_text, title_font_name, title_font_size)
    title_x = width - 500  # Posisi x untuk title
    title_y = height - 150  # Posisi y untuk title

    texts = [
        (title_text, "title", title_x, title_y),  # Tengah atas
        (f"{nama_lengkap}", "normal", 20, height - 200),  # Posisi yang ditentukan
        (f"{buku_dipilih}", "book", 20, height - 260),
        (f"{genre}", "bold", 20, height - 240),
        (f"{penulis}", "italic", 20, height - 280),
        (f"Tanggal Peminjaman   : {tanggal_pinjam}", "bottom", 20, height - 340),
        (f"Tanggal Pengembalian : {tanggal_kembali}", "bottom", 20, height - 370),
        (f"Kode Tiket : {random_code}", "bottom", 20, height - 400)
    ]

    # Draw each text with specified font style, position, and size
    for text, style, x, y in texts:
        font_name, font_size = font_styles[style]
        c.setFont(font_name, font_size)
        c.setFillColorRGB(1, 1, 1)  # Mengatur warna teks menjadi putih
        c.drawString(x, y, text)

    # Menambahkan QR code ke PDF di pojok kanan atas
    qr_width = 100  # Ukuran lebar QR code dalam pixel
    qr_height = 100  # Ukuran tinggi QR code dalam pixel
    qr_x = width - qr_width - 50  # Koordinat x untuk pojok kanan atas
    qr_y = height - qr_height - 20  # Koordinat y untuk pojok kanan atas
    c.drawImage(qr_filename, qr_x, qr_y, width=qr_width, height=qr_height)

    # Menambahkan gambar cover buku ke PDF di pojok kanan bawah
    cover_width = 125  # Ukuran lebar cover dalam pixel
    cover_height = 200  # Ukuran tinggi cover dalam pixel
    cover_x = width - cover_width - 50  # Koordinat x untuk pojok kanan bawah
    cover_y = height - qr_height - cover_height - 50  # Koordinat y untuk pojok kanan bawah
    c.drawImage(cover_path, cover_x, cover_y, width=cover_width, height=cover_height)

    # Hitung koordinat untuk garis
    x_start = 100  # Ujung kiri kertas A5
    y_start = A5[1] * 3/4  # 3/4 bagian dari atas kertas A5
    x_end = A5[0] - 100  # Ujung kanan kertas A5
    y_end = A5[1] * 3/4  # 3/4 bagian dari atas kertas A5

    # Set warna garis menjadi putih (RGB: 1, 1, 1)
    c.setStrokeColorRGB(1, 1, 1)

    # Gambar garis pada canvas dengan warna putih
    c.line(x_start, y_start, x_end, y_end)
    
    # Menyelesaikan PDF
    c.showPage()
    c.save()
    
    # Memanggil fungsi baru untuk mencetak tiket dan membuka tiket ke browser
    pdf_filename = print_and_open_ticket(c)

    # Menyimpan informasi tiket ke database
    save_loan_ticket_to_database(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali, pdf_filename)

    return pdf_filename

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
        msg.set_content(f"""
    Dear Valued Petron,

    Thank you for choosing PETI.

    Your PETI OTP verification code for account verification is: {otp}

    Please use this code to complete your account verification process. This code ensures the security of your account and helps us prevent unauthorized access.

    If you did not request this code or have any concerns regarding your account security, please contact our support team immediately at our support email.

    For your convenience and security, please do not share this code with anyone else.

    We appreciate your cooperation in maintaining the security of your PETI account.

    Best Regards,
    PETI Security Team

    Contact Information:
    e-Mail: petibyunsofficial@gmail.com
    """)
        
        server.send_message(msg)
        server.quit()
        print("Email sent")

    def back_login():
        window2.destroy()
        halaman_login()

    def login_user():
            global user_email
            email = entry_email.get()
            user_email = email
            password = entry_password.get()
            
            # Membaca data pengguna dari file CSV
            with open('database/databaseUser.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == email and row[2] == password:
                        window.destroy()  # Tutup halaman login
                        setup_home_screen(email)
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

if __name__ == "__main__":
    halaman_login()

script_dir = os.path.dirname(os.path.abspath(__file__))
detail_buku_frame = None
peminjaman_buku_frame = None

def kembali():
    detail_buku_frame.pack_forget()
    main_frame.pack(side=ctk.TOP, fill="both", expand=True)  # Menampilkan kembali frame utama

def pinjam_kembali():
    peminjaman_buku_frame.pack_forget()
    main_frame.pack(side=ctk.TOP, fill="both", expand=True)  # Menampilkan kembali frame utama

def tampilkan_peminjaman_buku(buku_dipilih, df):
    print("tampilkan_peminjaman_buku dipanggil")
    def show_calendar(button):
        if button == button_tanggal_pinjam:
            calendar_window = ctk.CTkToplevel(frame_tanggal_pinjam)
            calendar_window.geometry("300x300")
            calendar = Calendar(calendar_window, selectmode='day', date_pattern='dd-mm-yyyy')
            calendar.pack(pady=10)

        def get_date():
            selected_date = calendar.get_date()
            global tanggal_pinjam
            global tanggal_kembali
            
            if button == button_tanggal_pinjam:
                button_tampilkan_pinjam.configure(text=selected_date)
                tanggal_peminjaman = datetime.strptime(selected_date, "%d-%m-%Y").date()  # Ambil hanya bagian tanggal
                tanggal_pinjam = tanggal_peminjaman
                tanggal_pengembalian = tanggal_peminjaman + timedelta(days=7)
                tanggal_kembali = tanggal_pengembalian
                button_tampilkan_kembali.configure(text=tanggal_pengembalian.strftime("%d-%m-%Y"))
            elif button == button_tanggal_kembali:
                button_tampilkan_kembali.configure(text=selected_date)

            calendar_window.destroy()

        select_button = ctk.CTkButton(calendar_window, text="Select Date", command=get_date)
        select_button.pack(pady=10)
   
        calendar_window.lift()
        
        calendar_window.grab_set()

    try:
        if 'background' not in df.columns or 'cover' not in df.columns:
            print("Kolom 'cover' tidak ditemukan dalam file CSV.")
            return
        
        cover_path = buku_dipilih['cover']
        background_path = buku_dipilih['background']
        if os.path.exists(cover_path):
            try:
                cover_image = Image.open(cover_path)
                cover_image = cover_image.resize((350, 450))
                cover_photo = ImageTk.PhotoImage(cover_image)
            

            except Exception as e:
                print(f"Error loading image {cover_path}: {e}")
                cover_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="red"))  # Placeholder merah jika ada error
        else:
            print(f"Cover image not found: {cover_path}")
            cover_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="gray"))  # Placeholder abu-abu jika tidak ditemukan
        if os.path.exists(background_path):
            try:
                background_image = Image.open(background_path)
                bg_photo = ImageTk.PhotoImage(background_image)
            

            except Exception as e:
                print(f"Error loading image {background_path}: {e}")
                bg_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="red"))  # Placeholder merah jika ada error
        else:
            print(f"Cover image not found: {background_path}")
            bg_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="gray"))  # Placeholder abu-abu jika tidak ditemukan    

        global peminjaman_buku_frame
        peminjaman_buku_frame = ctk.CTkFrame(window_beranda, width=1200, height=600, fg_color="#1A1F23")
        peminjaman_buku_frame.pack(side="top", fill="both", expand=True)

        main_frame.pack_forget()
        category_frame.pack_forget()
        detail_buku_frame.pack_forget()

        bg_img_label = ctk.CTkLabel(peminjaman_buku_frame, image=bg_photo, text="")
        bg_img_label.place(relx=0.5, rely=0.15, anchor="center")

        cover_img_label = ctk.CTkLabel(peminjaman_buku_frame, image=cover_photo, text="")
        cover_img_label.place(relx=0.65, rely=0.5, anchor="center")
       
        frame_tanggal_pinjam = ctk.CTkFrame(peminjaman_buku_frame, width=500, height=60, corner_radius=10, 
                                            fg_color="#e3dfe6")
        frame_tanggal_pinjam.place(relx=0.3, rely=0.55, anchor="center")

        # Membuat tombol "Tanggal Peminjaman"
        button_tanggal_pinjam = ctk.CTkButton(peminjaman_buku_frame, width=250, height=40, corner_radius=10, 
                                              bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, 
                                              border_color="#a6a4a8", text="Tanggal Peminjaman", text_color="#000000", 
                                              font=("Trebuchet MS", 16), hover=True, hover_color="#AAAAAA")
        button_tanggal_pinjam.place(relx=0.23, rely=0.55, anchor="center")
        button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))  # Adjusted here

        # Tombol untuk menampilkan tanggal yang telah dipilih
        button_tampilkan_pinjam = ctk.CTkButton(peminjaman_buku_frame, width=150, height=40, corner_radius=10, 
                                                bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, 
                                                border_color="#e3dfe6", text="", text_color="#000000", 
                                                font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
        button_tampilkan_pinjam.place(relx=0.4, rely=0.55, anchor="center")
        button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))

        frame_tanggal_kembali = ctk.CTkFrame(peminjaman_buku_frame, width=500, height=60, corner_radius=10, 
                                             fg_color="#e3dfe6")
        frame_tanggal_kembali.place(relx=0.3, rely=0.65, anchor="center")

        # Membuat tombol "Tanggal Pengembalian"
        button_tanggal_kembali = ctk.CTkButton(peminjaman_buku_frame, width=250, height=40, corner_radius=10, 
                                               bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, 
                                               border_color="#a6a4a8", text="Tanggal Pengembalian", 
                                               text_color="#000000", font=("Trebuchet MS", 16), hover=True, 
                                               hover_color="#AAAAAA")
        button_tanggal_kembali.place(relx=0.23, rely=0.65, anchor="center")
        button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))  # Adjusted here

        # Tombol untuk menampilkan tanggal yang telah dipilih
        button_tampilkan_kembali = ctk.CTkButton(peminjaman_buku_frame, width=150, height=40, corner_radius=10, 
                                                 bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, 
                                                 border_color="#e3dfe6", text="", text_color="#000000", 
                                                 font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
        button_tampilkan_kembali.place(relx=0.4, rely=0.65, anchor="center")
        button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))

        # Membuat label untuk menampilkan tanggal pengembalian
        label_tanggal_kembali = ctk.CTkLabel(peminjaman_buku_frame, text="", font=("Trebuchet MS", 16), 
                                             bg_color="#e3dfe6", fg_color="#000000")
        label_tanggal_kembali.place(relx=0.6, rely=0.55, anchor="center")

        button_back = ctk.CTkButton(peminjaman_buku_frame, width=100, height=35, corner_radius=30, fg_color="#1A1F23", 
                                    border_width=0, text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), 
                                    hover=False, command=pinjam_kembali)
        button_back.place(relx=0.1, rely=0.1, anchor="e")

        button_cetak = ctk.CTkButton(peminjaman_buku_frame, width=200, height=50, corner_radius=10, 
                                     fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="CETAK", 
                                     text_color="#E3DFE6", font=("Trebuchet MS", 20), hover=True, hover_color="#A84F6C", command=lambda: save_loan_ticket_to_database(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali, pdf_filename))
        button_cetak.place(relx=0.3, rely=0.8, anchor="center")

    except FileNotFoundError as e:
        print("File Not Found", f"Error: {e}")

def tampilkan_detail_buku(buku_dipilih, df):
    try:
        if 'background' not in df.columns or 'cover' not in df.columns:
            print("Kolom 'cover' tidak ditemukan dalam file CSV.")
            return
        
        cover_path = buku_dipilih['cover']
        background_path = buku_dipilih['background']
        if os.path.exists(cover_path):
            try:
                cover_image = Image.open(cover_path)
                cover_image = cover_image.resize((350, 450))
                cover_photo = ImageTk.PhotoImage(cover_image)
            

            except Exception as e:
                print(f"Error loading image {cover_path}: {e}")
                cover_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="red"))  # Placeholder merah jika ada error
        else:
            print(f"Cover image not found: {cover_path}")
            cover_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="gray"))  # Placeholder abu-abu jika tidak ditemukan
        if os.path.exists(background_path):
            try:
                background_image = Image.open(background_path)
                bg_photo = ImageTk.PhotoImage(background_image)
            

            except Exception as e:
                print(f"Error loading image {background_path}: {e}")
                bg_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="red"))  # Placeholder merah jika ada error
        else:
            print(f"Cover image not found: {background_path}")
            bg_photo = ImageTk.PhotoImage(Image.new("RGB", (350, 450), color="gray"))  # Placeholder abu-abu jika tidak ditemukan    

        global detail_buku_frame
        detail_buku_frame = ctk.CTkFrame(window_beranda, width=1200, height=600, fg_color="#1A1F23")
        detail_buku_frame.pack(side="top", fill="both", expand=True)

        main_frame.pack_forget()
        category_frame.pack_forget()

        bg_img_label = ctk.CTkLabel(detail_buku_frame, image=bg_photo, text="")
        bg_img_label.place(relx=0.5, rely=0.15, anchor="center")

        cover_img_label = ctk.CTkLabel(detail_buku_frame, image=cover_photo, text="")
        cover_img_label.place(relx=0.15, rely=0.5, anchor="center")
        
        book_desc_frame = ctk.CTkFrame(detail_buku_frame, width=400, height=400, bg_color="#1A1F23", 
                                       fg_color="#1A1F23")
        book_desc_frame.place(relx=0.58, rely=0.7  , anchor="center")

        label_genre = ctk.CTkLabel(book_desc_frame, text=f"Genre: {buku_dipilih['genre']}", font=("Trebuchet MS", 16))
        label_genre.pack(side="top", anchor="w", pady=1, padx=10)

        label_judul = ctk.CTkLabel(book_desc_frame, text=f"Judul: {buku_dipilih['judul']}", font=("Trebuchet MS", 20))
        label_judul.pack(side="top", anchor="w", pady=1, padx=10)

        label_penulis = ctk.CTkLabel(book_desc_frame, text=f"Penulis: {buku_dipilih['penulis']}", 
                                     font=("Trebuchet MS", 12))
        label_penulis.pack(side="top", anchor="w", pady=1, padx=10)

        label_tahun = ctk.CTkLabel(book_desc_frame, text=f"Tahun Terbit: {buku_dipilih['tahunTerbit']}", 
                                   font=("Trebuchet MS", 12))
        label_tahun.pack(side="top", anchor="w", pady=5, padx=10)

        label_halaman = ctk.CTkLabel(book_desc_frame, text=f"Halaman: {buku_dipilih['halaman']}", 
                                     font=("Trebuchet MS", 12))
        label_halaman.pack(side="top", anchor="w", pady=5, padx=10)

        label_sinopsis = ctk.CTkLabel(book_desc_frame, text=f"Sinopsis: {buku_dipilih['sinopsis']}", 
                                      font=("Trebuchet MS", 12), wraplength=800)
        label_sinopsis.configure(justify="left")
        label_sinopsis.pack(side="top", anchor="w", pady=5, padx=10)
    
        label_stok = ctk.CTkLabel(book_desc_frame, text=f"Stok: {buku_dipilih['stok']}", font=("Trebuchet MS", 16))
        label_stok.pack(side="top", anchor="w", pady=5, padx=10)

        button_back = ctk.CTkButton(detail_buku_frame, width=100, height=35, corner_radius=30, fg_color="#1A1F23", 
                                    border_width=0, text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), 
                                    hover=False, command=kembali)
        button_back.place(relx=0.1, rely=0.1, anchor="e")

        borrow_button = ctk.CTkButton(detail_buku_frame, text="PINJAM", width=120, height=35, corner_radius=30, 
                                      fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", 
                                      hover=True, hover_color="#A84F6C", font=("Trebuchet MS", 16), 
                                      command=lambda: tampilkan_peminjaman_buku(buku_dipilih, df))
        borrow_button.place(relx=0.7, rely=0.5, anchor="w")
        
    except FileNotFoundError as e:
        print("File Not Found", f"Error: {e}")

# Fungsi untuk menampilkan daftar buku
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
            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", 
                                         command=lambda buku=row: tampilkan_detail_buku(buku, df))
            button_cover.image = cover_photo  # Menyimpan referensi gambar
            button_cover.pack(side="top")

            label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6", 
                                       wraplength=300)
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

            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", 
                                         command=lambda buku=row: tampilkan_detail_buku(buku, df))
            button_cover.image = cover_photo  # Menyimpan referensi gambar
            button_cover.pack(side="top")

            label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6", 
                                       wraplength=300)
            label_judul.pack(side="top")
    
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print(f"File '{file_path}' kosong atau tidak dapat dibaca.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def setup_home_screen():
    logo2_path = os.path.join(script_dir, "gambar/logo2.png")
    icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
    icon_acc_path = os.path.join(script_dir, "gambar/account_icon.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((320,117))
    logo2 = ImageTk.PhotoImage(resize_img)
    icon_search = Image.open(icon_search_path)
    resize_img = icon_search.resize((20,20))
    icon_search = ImageTk.PhotoImage(resize_img)
    icon_acc = Image.open(icon_acc_path)
    resize_img = icon_acc.resize((70,70))
    icon_acc = ImageTk.PhotoImage(resize_img)

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
        category_scrollable_frame = ctk.CTkScrollableFrame(category_frame, fg_color="#1A1F23", 
                                                           orientation="horizontal")
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

    option_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    option_frame.pack(side=ctk.TOP)
    option_frame.pack_propagate(False)
    option_frame.configure(width=1300, height=120)

    global main_frame
    main_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    main_frame.pack(side=ctk.TOP, fill="both", expand=True)
    main_frame.pack_propagate(False)
    main_frame.configure(width=1300, height=600) 

    global category_frame
    category_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    category_frame.pack_forget()
    category_frame.pack_propagate(False)
    category_frame.configure(width=1300, height=600)


    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
    l1.place(x=10, y=10, anchor="nw")

    button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_beranda)
    button1.place(relx=0.5, rely=0.055, anchor="center")

    button1_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", 
                                    fg_color="#1A1F23")
    button1_indicate.place(relx=0.5, rely=0.4, anchor="center")

    button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_kategori)
    button2.place(relx=0.63, rely=0.055, anchor="center")

    button2_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", 
                                    fg_color="#1A1F23")
    button2_indicate.place(relx=0.63, rely=0.4, anchor="center")

    button3 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Buku Saya", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30")
    button3.place(relx=0.76, rely=0.055, anchor="center")

    button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", 
                            fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
    button4.place(relx=0.95, rely=0.055, anchor="center")

    scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=1200, height=500, fg_color="#1A1F23", orientation="horizontal")
    scrollable_frame.pack(side="top", fill="both", expand=True)

    show_beranda()
    
window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x600")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True,True)

# Tampilkan daftar buku di scrollable frame

setup_home_screen()
window_beranda.mainloop()