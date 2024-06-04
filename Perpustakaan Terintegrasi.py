from customtkinter import *
import customtkinter as ctk
from tkinter import Text
from PIL import Image, ImageTk
import os
import random
import smtplib
import csv
import string
import qrcode
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pandas as pd
from email.message import EmailMessage
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A5, inch
from loginregist import register_user, login_user, menuDua

ctk.set_appearance_mode("dark")
script_dir = os.path.dirname(os.path.abspath(__file__))
detail_buku_frame = None
peminjaman_buku_frame = None
user_email = None
tanggal_pinjam = None
tanggal_kembali = None
pdf_filename = None

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
    # Ekstraksi judul buku jika buku_dipilih adalah Series atau DataFrame
    if isinstance(buku_dipilih, pd.Series):
        buku_dipilih = buku_dipilih.iloc[0]
    elif isinstance(buku_dipilih, pd.DataFrame):
        buku_dipilih = buku_dipilih['judul'].iloc[0]
    
    with open('database/databuku.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['judul'] == buku_dipilih:
                return row['cover']
    return None

def read_book_details(buku_dipilih):
    """Membaca genre dan penulis buku dari databuku.csv berdasarkan judul buku."""
    genre = None
    penulis = None

    # Ekstraksi judul buku jika buku_dipilih adalah Series atau DataFrame
    if isinstance(buku_dipilih, pd.Series):
        buku_dipilih = buku_dipilih.iloc[0]
    elif isinstance(buku_dipilih, pd.DataFrame):
        buku_dipilih = buku_dipilih['judul'].iloc[0]

    with open('database/databuku.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['judul'] == buku_dipilih:
                genre = row['genre']
                penulis = row['penulis']
                break

    return genre, penulis

def simpan_data_buku(data_buku):
    df = pd.DataFrame(data_buku)
    df.to_csv('database/databuku.csv', index=False)

def baca_data_buku():
    try:
        return pd.read_csv('database/databuku.csv').to_dict('records')
    except FileNotFoundError:
        return []

def save_loan_ticket_to_database(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali):
    # Fungsi untuk membaca data buku dari CSV
    def baca_data_buku():
        try:
            return pd.read_csv('database/databuku.csv').to_dict('records')
        except FileNotFoundError:
            return []

    # Fungsi untuk menyimpan data buku ke CSV
    def simpan_data_buku(data_buku):
        df = pd.DataFrame(data_buku)
        df.to_csv('database/databuku.csv', index=False)
    
    data_buku = baca_data_buku()

    # Kurangi stok buku yang dipilih dengan 1
    for buku in data_buku:
        if buku["judul"] == buku_dipilih["judul"]:
            buku["stok"] = int(buku["stok"]) - 1
            break

    # Simpan data buku yang telah diperbarui ke dalam file databuku.csv
    simpan_data_buku(data_buku)
    
    global pdf_filename
    """Menyimpan informasi tiket peminjaman ke database datapinjam.csv."""
    pdf_filename = create_loan_ticket(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali)
    fieldnames = ['email', 'judul', 'tanggalPinjam', 'tanggalKembali', 'tiket']

    # Ekstraksi judul buku jika buku_dipilih adalah DataFrame atau Series
    if isinstance(buku_dipilih, pd.Series):
        judul_buku = buku_dipilih['judul'].split(': ')[1] if 'judul:' in buku_dipilih['judul'] else buku_dipilih['judul']
    elif isinstance(buku_dipilih, pd.DataFrame):
        judul_buku = buku_dipilih['judul'].iloc[0].split(': ')[1] if 'judul:' in buku_dipilih['judul'].iloc[0] else buku_dipilih['judul'].iloc[0]
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

def create_loan_ticket(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali):
    """Membuat tiket peminjaman buku dalam bentuk PDF dan menyimpannya ke database."""
    # Mendapatkan genre dan penulis dari buku yang dipilih
    genre, penulis = read_book_details(buku_dipilih)
    
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
    pdf_filename = f"tiket/tiket_peminjaman_{random_code}.pdf"
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

    # Menyelesaikan PDF dan membuka tiket peminjaman
    c.showPage()
    c.save()
    print(f"Tiket peminjaman telah disimpan sebagai {pdf_filename}")
    webbrowser.open_new(f"file://{os.path.abspath(pdf_filename)}")

    return pdf_filename

def halaman_login():
    window = ctk.CTk()
    window.title("login")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")
    window.resizable(True,True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image1_path = os.path.join(script_dir, "gambar/storyboard1.png")
    logo_path = os.path.join(script_dir, "gambar/logo_peti.png")

    img1 = Image.open(image1_path)
    img1 = ImageTk.PhotoImage(img1)

    logo_img = Image.open(logo_path)
    resize_img = logo_img.resize((150, 150))
    logo_img = ImageTk.PhotoImage(resize_img)

    l1 = ctk.CTkLabel(window, image=img1, text="")
    l1.pack()

    frame = ctk.CTkFrame(window, width=350, height=500, corner_radius=0, fg_color="White")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    l2 = ctk.CTkLabel(window, image=logo_img, text="", bg_color="white", fg_color="transparent")
    l2.place(relx=0.5, rely=0.28, anchor="center")

    l3 = ctk.CTkLabel(frame, text="Login", text_color="#1A1F23", font=('Trebuchet MS', 40))
    l3.place(relx=0.5, rely=0.28, anchor="center")

    entry_email = ctk.CTkEntry(frame, width=300, height=35, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Email", font=('Trebuchet MS', 20), placeholder_text_color="#A6A4A8")
    entry_email.place(relx=0.5, rely=0.42, anchor="center")

    error_login = ctk.CTkLabel(frame, text="", text_color="red", font=('Trebuchet MS', 12))
    error_login.place(relx=0.59, rely=0.58, anchor="e")

    entry_password = ctk.CTkEntry(frame, width=300, height=35, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Password", font=('Trebuchet MS', 20), placeholder_text_color="#A6A4A8", show="*")
    entry_password.place(relx=0.5, rely=0.52, anchor="center")

    def halaman_register():
        window.destroy()
        global window2
        window2 = ctk.CTk()
        window2.title("register")
        screen_width = window2.winfo_screenwidth()
        screen_height = window2.winfo_screenheight()
        window2.geometry(f"{screen_width}x{screen_height}+0+0")
        window2.resizable(True,True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image1_path = os.path.join(script_dir, "gambar/storyboard1.png")
        logo_path = os.path.join(script_dir, "gambar/logo_peti.png")

        img1 = Image.open(image1_path)
        img1 = ImageTk.PhotoImage(img1)

        logo_img = Image.open(logo_path)
        resize_img = logo_img.resize((150, 150))
        logo_img = ImageTk.PhotoImage(resize_img)

        l1 = ctk.CTkLabel(window2, image=img1, text="")
        l1.pack()

        frame = ctk.CTkFrame(window2, width=700, height=500, corner_radius=0, fg_color="White")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        l2 = ctk.CTkLabel(window2, image=logo_img, text="", bg_color="white", fg_color="transparent")
        l2.place(relx=0.5, rely=0.28, anchor="center")

        l3 = ctk.CTkLabel(frame, text="Register", text_color="#1A1F23", font=('Trebuchet MS', 50))
        l3.place(relx=0.5, rely=0.28, anchor="center")

        entry_nama_lengkap = ctk.CTkEntry(frame, width=547, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Nama Lengkap", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8")
        entry_nama_lengkap.place(relx=0.5, rely=0.38, anchor="center")

        entry_alamat = ctk.CTkEntry(frame, width=547, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Alamat", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8")
        entry_alamat.place(relx=0.5, rely=0.45, anchor="center")

        entry_nomor_hp = ctk.CTkEntry(frame, width=547, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="No. HP", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8")
        entry_nomor_hp.place(relx=0.5, rely=0.52, anchor="center")

        entry_username = ctk.CTkEntry(frame, width=200, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Username", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8")
        entry_username.place(relx=0.268, rely=0.62, anchor="center")

        entry_email = ctk.CTkEntry(frame, width=200, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Email", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8")
        entry_email.place(relx=0.268, rely=0.68, anchor="center")

        entry_password = ctk.CTkEntry(frame, width=200, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Password", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8", show="*")
        entry_password.place(relx=0.732, rely=0.62, anchor="center")

        error_pw_regis = ctk.CTkLabel(frame, text="", text_color="red", font=('Trebuchet MS', 10))
        error_pw_regis.place(relx=0.772, rely=0.725, anchor="e")

        entry_konfirmasi_password = ctk.CTkEntry(frame, width=200, height=27, corner_radius=30, fg_color="White", border_width=2, border_color="#E3DFE6", text_color="#242C32", placeholder_text="Konfirmasi Password", font=('Trebuchet MS', 16), placeholder_text_color="#A6A4A8", show="*")
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

        button2 = ctk.CTkButton(frame, width=170, height=20, fg_color="transparent", border_width=0, text="Login", text_color="#A84F6C", font=("Trebuchet MS", 12), hover=False, command=back_login)
        button2.place(relx=0.55, rely=0.87, anchor="center")

        l4 = ctk.CTkLabel(frame, text="Sudah punya akun?", text_color="#1A1F23", font=('Trebuchet MS', 12))
        l4.place(relx=0.45, rely=0.87, anchor="center")

        button1 = ctk.CTkButton(frame, width=547, height=27, corner_radius=30, fg_color="#A84F6C", border_width=0, text="Daftar", text_color="White", font=("Trebuchet MS", 18), hover=True, hover_color="#66273B", command=register_user)
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

    def send_reminder(to_mail, book_title, due_date, ticket_path):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        from_mail = "petibyunsofficial@gmail.com"
        server.login(from_mail, "johl erdn chfr jdgq")
        
        msg = EmailMessage()
        msg["Subject"] = "Book Return Reminder"
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg.set_content(f"""
    Dear Valued Patron,

    We hope this message finds you well. This is a friendly reminder that the book titled "{book_title}" you borrowed from our library is due on {due_date}.

    To ensure that all patrons have fair access to our resources, we kindly ask that you return the book by the due date. Late returns may incur penalties as per our library policy, which is detailed on our website.

    Attached to this email is a copy of your borrowing ticket for your reference. Please keep this ticket for your records. If you have any questions or need to extend your borrowing period, do not hesitate to contact us at your earliest convenience. We are here to assist you.

    Thank you for your cooperation and continued support of our library. We look forward to serving you again.

    Best Regards,
    The PETI Library Team

    Contact Information:
    e-Mail: petibyunsofficial@gmail.com
    """)
        
        # Attach the ticket image
        with open(ticket_path, 'rb') as file:
            msg.add_attachment(file.read(), maintype='image', subtype='jpeg', filename=os.path.basename(ticket_path))
        
        server.send_message(msg)
        server.quit()
        print(f"Reminder email sent to {to_mail}")

    def send_due_date_reminders():
        try:
            reminder_date = datetime.today().date() + timedelta(days=3)
            
            with open('database/datapinjam.csv', mode='r') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    email = row['email']
                    book_title = row['judul']
                    due_date_str = row['tanggalKembali']
                    ticket_path = row['tiket']
                    
                    # Pastikan tanggal pengembalian tidak None dan sesuai format
                    if due_date_str and '-' in due_date_str:
                        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        
                        if due_date == reminder_date and ticket_path:
                            formatted_due_date = due_date.strftime("%Y-%m-%d")
                            send_reminder(email, book_title, formatted_due_date, ticket_path)
                            print("Reminder terkirim")
                    else:
                        print(f"Invalid due date format or missing date for book {book_title}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
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
                        window.destroy()
                        send_due_date_reminders()
                        setup_home_screen(email)
                        return email  # Mengembalikan email pengguna saat login berhasil
            
            error_login.configure(text="Email atau password tidak sesuai")
            return None  # Mengembalikan None jika login gagal
            
    button1 = ctk.CTkButton(frame, width=300, height=35, corner_radius=30, fg_color="#A84F6C", border_width=0, text="Login", text_color="White", font=("Trebuchet MS", 20), hover=True, hover_color="#66273B",  command=login_user)
    button1.place(relx=0.5, rely=0.65, anchor="center")

    button2 = ctk.CTkButton(frame, width=35, height=35, fg_color="transparent", border_width=0, text="Daftar", text_color="#A84F6C", font=("Trebuchet MS", 12), hover=False, command=halaman_register)
    button2.place(relx=0.63, rely=0.723, anchor="center")

    l4 = ctk.CTkLabel(frame, text="Belum punya akun?", text_color="#1A1F23", font=('Trebuchet MS', 12))
    l4.place(relx=0.39, rely=0.72, anchor="center")

    window.mainloop()

if __name__ == "__main__":
    halaman_login()



# Fungsi untuk membaca data pinjaman dari CSV
def baca_data_pinjam():
    try:
        return pd.read_csv('database/datapinjam.csv').to_dict('records')
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data pinjaman ke CSV
def simpan_data_pinjam(data_pinjam):
    df = pd.DataFrame(data_pinjam)
    df.to_csv('database/datapinjam.csv', index=False)

# Fungsi untuk mengembalikan buku yang dipinjam
def kembalikan_buku(user_email, judul_buku):
    data_buku = baca_data_buku()
    data_pinjam = baca_data_pinjam()
    buku_ketemu = False
    
    for buku in data_buku:
        if buku["judul"] == judul_buku:
            buku_ketemu = True
            buku["stok"] = int(buku["stok"]) + 1
            data_pinjam = [pinjam for pinjam in data_pinjam if not (pinjam["email"] == user_email and pinjam["judul"] == judul_buku)]

            simpan_data_buku(data_buku)
            simpan_data_pinjam(data_pinjam)

            print(f"Buku '{judul_buku}' berhasil dikembalikan.")
            display_data(user_email)  # Update display after returning a book
            return
    
    if not buku_ketemu:
        print(f"Buku '{judul_buku}' tidak ditemukan.")

def display_data(user_email):
    data = baca_data_pinjam()
    user_data = [pinjam for pinjam in data if pinjam['email'] == user_email]

    for widget in frame_data.winfo_children():
        widget.destroy()
    
    if user_data:
        for row in user_data:
            frame_entry = ctk.CTkFrame(frame_data, fg_color="#232A30")
            frame_entry.pack(pady=5, padx=5, fill='x')
            
            ctk.CTkLabel(frame_entry, text=f"Judul: {row['judul']} | Tanggal Pinjam: {row['tanggalPinjam']} | Tanggal Kembali: {row['tanggalKembali']}").pack(side='left')
            ctk.CTkButton(frame_entry, fg_color="#1A1F23", corner_radius=30, hover=True, hover_color="#232A30", text="Kembalikan", command=lambda r=row: kembalikan_buku(user_email, r['judul'])).pack(side='right')
    else:
        ctk.CTkLabel(frame_data, text="No records found").pack(anchor='w')

def search():
    display_data(user_email)

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
                tanggal_peminjaman = datetime.strptime(selected_date, "%d-%m-%Y").date()
                tanggal_pinjam = tanggal_peminjaman
                tanggal_pengembalian = tanggal_peminjaman + timedelta(days=7)
                tanggal_kembali = tanggal_pengembalian
                button_tampilkan_pinjam.configure(text=tanggal_pinjam.strftime("%d-%m-%Y"))
                button_tampilkan_kembali.configure(text=tanggal_pengembalian.strftime("%d-%m-%Y"))
            elif button == button_tanggal_kembali:
                tanggal_pengembalian = datetime.strptime(selected_date, "%d-%m-%Y").date()
                tanggal_kembali = tanggal_pengembalian
                button_tampilkan_kembali.configure(text=tanggal_kembali.strftime("%d-%m-%Y"))

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

        button_cetak = ctk.CTkButton(peminjaman_buku_frame, width=200, height=50, corner_radius=30, 
                                     fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="CETAK", 
                                     text_color="#E3DFE6", font=("Trebuchet MS", 20), hover=True, hover_color="#A84F6C", command=lambda : save_loan_ticket_to_database(user_email, buku_dipilih, tanggal_pinjam, tanggal_kembali))
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
        book_desc_frame.place(relx=0.58, rely=0.6 , anchor="center")

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
            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", hover=True, hover_color="#E3DFE6",
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

            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", hover=True, hover_color="#E3DFE6",
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
    icon_logout_path = os.path.join(script_dir, "gambar/logout.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((320,117))
    logo2 = ImageTk.PhotoImage(resize_img)
    icon_logout = Image.open(icon_logout_path)
    resize_img = icon_logout.resize((70,70))
    logout = ImageTk.PhotoImage(resize_img)

    def indicate(label):
        button1_indicate.configure(fg_color="#1A1F23")
        button2_indicate.configure(fg_color="#1A1F23")
        button3_indicate.configure(fg_color="#1A1F23")
        # Highlight the selected indicator
        label.configure(fg_color="#A84F6C")
        
    def show_beranda():
        indicate(button1_indicate)
        category_frame.pack_forget()
        buku_saya_frame.pack_forget()
        main_frame.pack(side=ctk.TOP, fill="both", expand=True)
        tampilkan_daftar_buku(scrollable_frame)
    
    def show_buku_saya():
        indicate(button3_indicate)
        category_frame.pack_forget()
        main_frame.pack_forget()
        buku_saya_frame.pack(side=ctk.TOP, fill="both", expand=True)
        display_data(user_email)

    def show_kategori():
        indicate(button2_indicate)
        main_frame.pack_forget()
        buku_saya_frame.pack_forget()
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

    global buku_saya_frame
    buku_saya_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")
    buku_saya_frame.pack(side=ctk.TOP, fill="both", expand=True)


    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
    l1.place(x=10, y=10, anchor="nw")

    button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_beranda)
    button1.place(relx=0.5, rely=0.055, anchor="center")

    button1_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", 
                                    fg_color="#1A1F23")
    button1_indicate.place(relx=0.5, rely=0.52, anchor="center")

    button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_kategori)
    button2.place(relx=0.63, rely=0.055, anchor="center")

    button2_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", 
                                    fg_color="#1A1F23")
    button2_indicate.place(relx=0.654, rely=0.52, anchor="center")

    button3 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                            text="Buku Saya", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                            hover_color="#232A30", command=show_buku_saya)
    button3.place(relx=0.76, rely=0.055, anchor="center")

    button3_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", 
                                    fg_color="#1A1F23")
    button3_indicate.place(relx=0.8075, rely=0.52, anchor="center")

    button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=logout, corner_radius=0, bg_color="#1A1F23", 
                            fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30", command=sys.exit)
    button4.place(relx=0.93, rely=0.055, anchor="center")

    scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=1200, height=500, fg_color="#1A1F23", orientation="horizontal")
    scrollable_frame.pack(side="top", fill="both", expand=True)

    frame_input = ctk.CTkFrame(buku_saya_frame, fg_color="#232A30")
    frame_input.pack(pady=10)

    ctk.CTkLabel(frame_input, text=f"Buku {user_email}", font=("Trebuchet MS", 20)).pack(anchor='w')
    ctk.CTkButton(frame_input, fg_color="#A84F6C",hover=True, hover_color="#232A30", text="Buku Saya", command=search).pack(pady=5)

    global frame_data
    frame_data = ctk.CTkFrame(buku_saya_frame, fg_color="#1A1F23")
    frame_data.pack(pady=10, fill='both', expand=True)
    show_beranda()
    
window_beranda = ctk.CTk()
window_beranda.title("Beranda")
screen_width = window_beranda.winfo_screenwidth()
screen_height = window_beranda.winfo_screenheight()
window_beranda.geometry(f"{screen_width}x{screen_height}+0+0")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True,True)

# Tampilkan daftar buku di scrollable frame

setup_home_screen()
window_beranda.mainloop()