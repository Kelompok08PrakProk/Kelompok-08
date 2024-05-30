import random
import string
import qrcode
import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A5, inch

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

def read_book_cover(buku_dipilih):
    """Membaca path gambar cover buku dari databuku.csv berdasarkan judul buku."""
    with open('database/databuku.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['judul'] == buku_dipilih:
                return row['cover']
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

# Uji fungsi create_loan_ticket
create_loan_ticket(email, "Laut Bercerita", "Fantasy", "J.K. Rowling", "2024-05-30", "2024-06-30")
