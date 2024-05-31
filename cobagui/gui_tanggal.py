import customtkinter as ctk
import qrcode
import random
import webbrowser
import os
import csv
import string
from PIL import Image, ImageTk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A5, inch
from reportlab.lib.utils import ImageReader

def kembali():
    # Contoh tindakan ketika tombol kembali ditekan
    print("Tombol Kembali ditekan")
    window_beranda.destroy()

def show_calendar(button):
    if button == button_tanggal_pinjam:
        calendar_window = ctk.CTkToplevel(frame_tanggal_pinjam)
        calendar_window.geometry("300x300")
        calendar = Calendar(calendar_window, selectmode='day', date_pattern='dd-mm-yyyy')
        calendar.pack(pady=10)

    def get_date():
        selected_date = calendar.get_date()
        
        if button == button_tanggal_pinjam:
            button_tampilkan_pinjam.configure(text=selected_date)
            tanggal_peminjaman = datetime.strptime(selected_date, "%d-%m-%Y")
            tanggal_pengembalian = tanggal_peminjaman + timedelta(days=7)
            button_tampilkan_kembali.configure(text=tanggal_pengembalian.strftime("%d-%m-%Y"))
        elif button == button_tanggal_kembali:
            button_tampilkan_kembali.configure(text=selected_date)

        calendar_window.destroy()

    select_button = ctk.CTkButton(calendar_window, text="Select Date", command=get_date)
    select_button.pack(pady=10)

    # Angkat jendela kalender ke depan
    calendar_window.lift()
    # Jadikan jendela kalender sebagai jendela utama sementarat
    calendar_window.grab_set()

def get_date():
    pass 

def change_book(book_info):
    cover_buku_path = os.path.join(script_dir, book_info["cover_path"])
    cover_buku = ctk.CTkImage(light_image=Image.open(cover_buku_path), size=(250, 350))
    cover_buku_label.configure(image=cover_buku)
    judul_buku_label.configure(text=book_info["title"])

def pinjam_buku(book_info):
    print(f"Buku '{book_info['title']}' dipinjam!")
    # Tambahkan logika peminjaman buku di sini

email = "dimasadira45@gmail.com"

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

def create_loan_ticket(user_email, buku_dipilih, genre, penulis, tanggal_pinjam, tanggal_kembali):
    """Membuat tiket peminjaman buku dalam bentuk PDF."""
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
    
    print(f"Tiket peminjaman telah disimpan sebagai {pdf_filename}")
    webbrowser.open_new(f"file://{os.path.abspath(pdf_filename)}")

# Membuat jendela utama
window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x800")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True, True) 

# Mendapatkan direktori skrip
script_dir = os.path.dirname(os.path.abspath(__file__))
logo2_path = os.path.join(script_dir, "gambar/logo2.png")
icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
icon_acc_path = os.path.join(script_dir, "gambar/account_icon.png")
cover_buku_path = os.path.join(script_dir, "gambar/cover buku/31.png")  # Path ke gambar sampul buku
background_cover_path = os.path.join(script_dir, "gambar/Background/Novel/Laut Bercerita.jpg")

# Memuat dan mengubah ukuran gambar logo

# Memuat gambar sampul buku
cover_buku = ctk.CTkImage(light_image=Image.open(cover_buku_path), size=(250, 350))
logo2 = ctk.CTkImage(light_image=Image.open(logo2_path), size=(200, 100))
background_cover = ctk.CTkImage(light_image=Image.open(background_cover_path), size=(3000, 200))
icon_search = ctk.CTkImage(light_image=Image.open(icon_search_path), size=(15, 8))
icon_acc = ctk.CTkImage(light_image=Image.open(icon_acc_path), size=(50, 50))
# Membuat label untuk logo
l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
l1.pack(pady=0, anchor="nw")

# Background covernya
background_cover = ctk.CTkLabel(window_beranda, image=background_cover, text="", bg_color="transparent", fg_color="transparent")
background_cover.place(relx=0, rely=0.25, anchor="center")

# Membuat tombol "Beranda"
button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
button1.place(relx=0.5, rely=0.055, anchor="center")

# Membuat tombol "Kategori"
button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
button2.place(relx=0.63, rely=0.055, anchor="center")

# Membuat entry untuk pencarian
entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", border_width=0, text_color="#1A1F23", placeholder_text="Search", font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
entry1.place(relx=0.81, rely=0.055, anchor="center")

# Membuat tombol pencarian
button3 = ctk.CTkButton(window_beranda, width=30, height=20, image=icon_search, corner_radius=0, bg_color="#9C909D", fg_color="#9C909D", border_width=0, text="", hover=False)
button3.place(relx=0.867, rely=0.055, anchor="center")

# Membuat tombol akun
button4 = ctk.CTkButton(window_beranda, width=70, height=70, image=icon_acc, corner_radius=0, bg_color="#1A1F23", fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
button4.place(relx=0.95, rely=0.055, anchor="center")


# Membuat tombol "Kembali"
button_back = ctk.CTkButton(window_beranda, width=100, height=35, corner_radius=0, fg_color="#1A1F23", border_width=0, border_color="", text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=False, command=kembali)
button_back.place(relx=0.08, rely=0.16, anchor="w")
frame_tanggal_pinjam = ctk.CTkFrame(window_beranda, width=500, height=60, corner_radius=10, fg_color="#e3dfe6")
frame_tanggal_pinjam.place(relx=0.3, rely=0.55, anchor="center")

# Membuat tombol "Tanggal Peminjaman"
button_tanggal_pinjam = ctk.CTkButton(window_beranda, width=250, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, border_color="#a6a4a8", text="Tanggal Peminjaman", text_color="#000000", font=("Trebuchet MS", 16), hover=True, hover_color="#AAAAAA")
button_tanggal_pinjam.place(relx=0.23, rely=0.55, anchor="center")
button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))  # Adjusted here

# Tombol untuk menampilkan tanggal yang telah dipilih
button_tampilkan_pinjam = ctk.CTkButton(window_beranda, width=150, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, border_color="#e3dfe6", text="", text_color="#000000", font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
button_tampilkan_pinjam.place(relx=0.4, rely=0.55, anchor="center")
button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))

frame_tanggal_kembali = ctk.CTkFrame(window_beranda, width=500, height=60, corner_radius=10, fg_color="#e3dfe6")
frame_tanggal_kembali.place(relx=0.3, rely=0.65, anchor="center")

# Membuat tombol "Tanggal Pengembalian"
button_tanggal_kembali = ctk.CTkButton(window_beranda, width=250, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, border_color="#a6a4a8", text="Tanggal Pengembalian", text_color="#000000", font=("Trebuchet MS", 16), hover=True, hover_color="#AAAAAA")
button_tanggal_kembali.place(relx=0.23, rely=0.65, anchor="center")
button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))  # Adjusted here

# Tombol untuk menampilkan tanggal yang telah dipilih
button_tampilkan_kembali = ctk.CTkButton(window_beranda, width=150, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, border_color="#e3dfe6", text="", text_color="#000000", font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
button_tampilkan_kembali.place(relx=0.4, rely=0.65, anchor="center")
button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))

# Membuat label untuk menampilkan tanggal pengembalian
label_tanggal_kembali = ctk.CTkLabel(window_beranda, text="", font=("Trebuchet MS", 16), bg_color="#e3dfe6", fg_color="#000000")
label_tanggal_kembali.place(relx=0.6, rely=0.55, anchor="center")

def cetak_tiket():
    user_email = "dimasadira45@gmail.com"  # Ganti dengan email pengguna yang sebenarnya
    buku_dipilih = judul_buku_label.cget("text")
    genre = "Novel"  # Ganti dengan genre yang sesuai
    penulis = "Penulis Buku"  # Ganti dengan nama penulis yang sesuai
    tanggal_pinjam = button_tampilkan_pinjam.cget("text")
    tanggal_kembali = button_tampilkan_kembali.cget("text")
    
    if tanggal_pinjam and tanggal_kembali:
        create_loan_ticket(user_email, buku_dipilih, genre, penulis, tanggal_pinjam, tanggal_kembali)
    else:
        print("Harap pilih tanggal peminjaman dan tanggal pengembalian.")

# Membuat tombol "Cetak"
button_cetak = ctk.CTkButton(window_beranda, width=200, height=50, corner_radius=10, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="CETAK", text_color="#E3DFE6", font=("Trebuchet MS", 20), hover=True, hover_color="#A84F6C", command=cetak_tiket)
button_cetak.place(relx=0.3, rely=0.8, anchor="center")

# Menampilkan gambar sampul buku
cover_buku_label = ctk.CTkLabel(window_beranda, image=cover_buku, text="", bg_color="transparent", fg_color="transparent")
cover_buku_label.place(relx=0.69, rely=0.5, anchor="center")

# Menambahkan judul buku
judul_buku_label = ctk.CTkLabel(window_beranda, text="Laut Bercerita", font=("Trebuchet MS", 30), text_color="#E3DFE6", bg_color="transparent", fg_color="transparent", padx=0, pady=0)
judul_buku_label.place(relx=0.69, rely=0.8, anchor="center")

window_beranda.mainloop()