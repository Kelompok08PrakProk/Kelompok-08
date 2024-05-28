import csv
import random
import string
import smtplib
import datetime
import qrcode
import pandas as pd
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from email.message import EmailMessage

# Fungsi untuk mengirim OTP
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

# Fungsi untuk registrasi pengguna
def register_user():
    # Mengambil input dari pengguna
    username = input("Username: ")
    email = input("Email: ")
    password1 = input("Password: ")
    password2 = input("Confirm Password: ")
    namalengkap = input("Full Name: ")
    alamat = input("Address: ")
    nomorHP = input("Phone Number: ")
    
    # Memastikan password cocok
    if password1 != password2:
        print("Passwords do not match. Please try again.")
        return
    
    # Membuat OTP
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Mengirim OTP ke email pengguna
    send_otp(email, otp)
    
    # Verifikasi OTP dari pengguna
    user_otp = input("Enter the OTP sent to your email: ")
    if user_otp != otp:
        print("Invalid OTP. Registration failed.")
        return
    
    # Menyimpan data pengguna ke dalam file CSV
    with open('database/databaseUser.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password1, namalengkap, alamat, nomorHP])
    
    print("Registration successful")

# Fungsi untuk login pengguna
def login_user():
    print("===  Login Page  ===")
    email = input("e-Mail: ")
    password = input("Password: ")
    
    # Membaca data pengguna dari file CSV
    with open('database/databaseUser.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email and row[2] == password:
                print("Login successful")
                return email  # Mengembalikan email pengguna saat login berhasil
    
    print("Invalid email or password")
    return None  # Mengembalikan None jika login gagal

def tampilkan_daftar_buku(file_path='database/databuku.csv'):
    try:
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Memeriksa apakah kolom 'judul' ada dalam DataFrame
        if 'judul' not in df.columns:
            print("Kolom 'judul' tidak ditemukan dalam file CSV.")
            return
        
        # Menampilkan daftar buku
        print("Daftar Buku yang Tersedia:")
        for idx, judul in enumerate(df['judul'], start=1):
            print(f"{idx}. {judul}")
    
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print(f"File '{file_path}' kosong atau tidak dapat dibaca.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tampilkan_buku_berdasarkan_genre(genre, file_path='database/databuku.csv'):
    try:
        # Membaca file CSV
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Filter buku berdasarkan genre
        buku_genre = df[df['genre'].str.lower() == genre.lower()]
        
        if buku_genre.empty:
            print(f"Tidak ada buku dengan genre '{genre}' yang ditemukan.")
        else:
            print(f"Daftar buku dengan genre '{genre}':")
            for index, row in buku_genre.iterrows():
                print(f"Judul: {row['judul']}, Penulis: {row['penulis']}, Tahun Terbit: {row['tahunTerbit']}, Halaman: {row['halaman']}")
                print(f"Sinopsis: {row['sinopsis']}")
                print(f"Stok: {row['stok']}\n")
                
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tampilkan_menu():
    print("Pilih genre buku yang ingin ditampilkan:")
    print("1. Novel")
    print("2. Cerpen")
    print("3. Biografi")
    print("4. Majalah")
    print("5. Kamus")
    print("6. Komik")
    print("7. Ensiklopedia")
    
    pilihan = input("Masukkan nomor genre yang ingin Anda tampilkan: ")
    
    genre_dict = {
        "1": "Novel",
        "2": "Cerpen",
        "3": "Biografi",
        "4": "Majalah",
        "5": "Kamus",
        "6": "Komik",
        "7": "Ensiklopedia"
    }
    
    genre = genre_dict.get(pilihan, None)
    
    if genre:
        tampilkan_buku_berdasarkan_genre(genre)
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")

def cari_buku(file_path='database/databuku.csv'):
    judul_dicari = input("Masukkan judul buku yang dicari: ").strip().lower()
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

def tampilkan_profil(user_email, file_path='database/databaseUser.csv', data_pinjam_path='database/datapinjam.csv'):
    try:
        # Pastikan user_email adalah string dan bukan boolean
        if not isinstance(user_email, str):
            print("Email tidak valid.")
            return
        
        # Membaca file CSV untuk data pengguna
        df_user = pd.read_csv(file_path, encoding="windows-1252")
        
        # Mencari data pengguna berdasarkan email
        user_data = df_user[df_user['email'].str.lower() == user_email.lower()]
        
        if user_data.empty:
            print("Data pengguna tidak ditemukan.")
        else:
            user_info = user_data.iloc[0]
            print("Menu Profil:")
            print("1. Akun")
            print("2. Data Peminjaman")
            
            # Meminta input nomor menu dari pengguna
            pilihan = input("Pilih menu (masukkan angka): ")
            if pilihan == '1':
                print(f"Nama Lengkap: {user_info['namalengkap']}")
                print(f"Alamat: {user_info['alamat']}")
                print(f"Nomor HP: {user_info['nomorHP']}")
            elif pilihan == '2':
                tampilkan_data_pinjaman(user_email, data_pinjam_path)
            else:
                print("Menu tidak valid.")
                
    except FileNotFoundError:
        print(f"File tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tampilkan_data_pinjaman(user_email, file_path='database/datapinjam.csv'):
    try:
        with open(file_path, newline='') as file:
            reader = csv.DictReader(file)
            data_pinjam = []
            for row in reader:
                if row['email'] == user_email:
                    data_pinjam.append(row)
            
            if not data_pinjam:
                print("Tidak ada data peminjaman untuk email tersebut.")
            else:
                print("Data peminjaman untuk email", user_email)
                for data in data_pinjam:
                    print("Judul:", data['judul'])
                    print("Tanggal Pinjam:", data['tanggalPinjam'])
                    print("Tanggal Kembali:", data['tanggalKembali'])
                    print("------------------------")
    
    except FileNotFoundError:
        print("File datapinjam.csv tidak ditemukan.")

def baca_data_buku():
  """Membaca data buku dari file CSV dan mengembalikannya sebagai daftar kamus."""
  data_buku = []
  with open('database/databuku.csv', encoding='windows-1252') as file:
    reader = csv.DictReader(file)
    for row in reader:
      data_buku.append(row)
  return data_buku

def tampilkan_daftar_buku(data_buku):
  """Menampilkan daftar buku dari daftar kamus."""
  print("Daftar Buku yang Tersedia:")
  for i, buku in enumerate(data_buku):
    nomor = i + 1
    judul = buku["judul"]
    print(f"{nomor}. {judul}")

def pilih_buku(data_buku):
  """Meminta pengguna untuk memilih nomor buku dan mengembalikan kamus buku yang dipilih."""
  while True:
    try:
      nomor_buku = int(input("Masukkan nomor buku yang ingin dilihat: "))
      if 1 <= nomor_buku <= len(data_buku):
        return data_buku[nomor_buku - 1]
      else:
        print("Nomor buku tidak valid. Silakan masukkan kembali.")
    except ValueError:
      print("Input tidak valid. Harap masukkan angka.")

def tampilkan_detail_buku(buku):
  """Menampilkan detail buku dari kamus buku."""
  print(f"\n**Detail Buku:**")
  print(f"Judul: {buku['judul']}")
  print(f"Genre: {buku['genre']}")
  print(f"Penulis: {buku['penulis']}")
  print(f"Tahun Terbit: {buku['tahunTerbit']}")
  print(f"Halaman: {buku['halaman']}")
  print(f"Sinopsis: {buku['sinopsis']}")
  print(f"Stok: {buku['stok']}")

def baca_data_buku():
    """Membaca data buku dari file databuku.csv"""
    data_buku = []
    with open('database/databuku.csv', mode='r', encoding='windows-1252') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_buku.append(row)
    return data_buku

def simpan_data_buku(data_buku):
    """Menyimpan data buku ke file databuku.csv"""
    with open('database/databuku.csv', mode='w', encoding='windows-1252', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["judul", "genre", "penulis", "tahunTerbit","halaman","sinopsis","stok"])
        writer.writeheader()
        for buku in data_buku:
            writer.writerow(buku)

def simpan_data_pinjam(data_pinjam):
    """Menyimpan data peminjaman ke file datapinjam.csv"""
    with open('database/datapinjam.csv', mode='w', encoding='windows-1252', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["email", "judul", "tanggalPinjam", "tanggalKembali"])
        writer.writeheader()
        for pinjam in data_pinjam:
            writer.writerow(pinjam)

def kembalikan_buku(user_email, judul_buku):
    """Mengembalikan buku yang telah dipinjam dan memperbarui stok buku."""
    # Baca data buku dan data peminjaman
    data_buku = baca_data_buku()
    data_pinjam = baca_data_pinjam()

    # Cari buku yang dikembalikan dan tambah stoknya
    for buku in data_buku:
        if buku["judul"] == judul_buku:
            buku["stok"] = int(buku["stok"]) + 1
            break
    else:
        print(f"Buku '{judul_buku}' tidak ditemukan dalam database.")
        return

    # Hapus catatan peminjaman dari data_pinjam
    data_pinjam = [pinjam for pinjam in data_pinjam if not (pinjam["email"] == user_email and pinjam["judul"] == judul_buku)]

    # Simpan data buku yang telah diperbarui dan data peminjaman yang telah diperbarui
    simpan_data_buku(data_buku)
    simpan_data_pinjam(data_pinjam)

    print(f"Buku '{judul_buku}' berhasil dikembalikan.")

def pinjam_buku(user_email, buku_dipilih):
    """Mencatat data peminjaman buku ke database datapinjam.csv."""
    while True:
        try:
            # Meminta input tanggal pinjam dari pengguna
            tanggal_pinjam_str = input("Masukkan tanggal pinjam (YYYY-MM-DD): ")
            # Mengubah format tanggal ke objek datetime.date
            tanggal_pinjam = datetime.strptime(tanggal_pinjam_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Format tanggal tidak valid. Silakan masukkan YYYY-MM-DD.")

    # Menghitung tanggal kembali (7 hari setelah tanggal pinjam)
    tanggal_kembali = tanggal_pinjam + timedelta(days=7)

    # Baca data buku
    data_buku = baca_data_buku()

    # Kurangi stok buku yang dipilih dengan 1
    for buku in data_buku:
        if buku["judul"] == buku_dipilih["judul"]:
            buku["stok"] = int(buku["stok"]) - 1
            break

    # Simpan data buku yang telah diperbarui ke dalam file databuku.csv
    simpan_data_buku(data_buku)

    data_pinjam = {
        "email": user_email,
        "judul": buku_dipilih["judul"],
        "tanggalPinjam": tanggal_pinjam.strftime("%Y-%m-%d"),
        "tanggalKembali": tanggal_kembali.strftime("%Y-%m-%d")
    }

    with open('database/datapinjam.csv', 'a', encoding='windows-1252', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["email", "judul", "tanggalPinjam", "tanggalKembali"])
        if file.tell() == 0:
            writer.writeheader()  # Tulis header jika file kosong
        writer.writerow(data_pinjam)

    print(f"Buku '{buku_dipilih['judul']}' berhasil dipinjam.")
    print(f"Tanggal pinjam: {tanggal_pinjam.strftime('%Y-%m-%d')}")
    print(f"Tanggal kembali: {tanggal_kembali.strftime('%Y-%m-%d')}")

def baca_data_pinjam():
    """Membaca data peminjaman dari file datapinjam.csv"""
    data_pinjam = []
    with open('database/datapinjam.csv', mode='r', encoding='windows-1252') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_pinjam.append(row)
    return data_pinjam

def baca_data_user(user_email):
  """Membaca data user dari file CSV dan mengembalikannya sebagai kamus."""
  with open('databaseUser.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
      if row["email"] == user_email:
        return row
  return None

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
    # Membaca nama lengkap pengguna dari database
    nama_lengkap = read_user_data(user_email)
    if not nama_lengkap:
        print(f"Pengguna dengan email {user_email} tidak ditemukan.")
        return
    
    # Menghasilkan kode random dan QR code
    random_code = generate_random_code()
    qr_filename = f"{random_code}.png"
    generate_qr_code(random_code, qr_filename)
    
    # Membuat PDF
    pdf_filename = f"tiket_peminjaman_{random_code}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Menambahkan teks ke PDF
    c.drawString(100, 750, f"Tiket Peminjaman Buku")
    c.drawString(100, 735, f"Nama Lengkap: {nama_lengkap}")
    c.drawString(100, 720, f"Judul Buku: {buku_dipilih}")
    c.drawString(100, 705, f"Genre: {genre}")
    c.drawString(100, 690, f"Penulis: {penulis}")
    c.drawString(100, 675, f"Tanggal Peminjaman: {tanggal_pinjam}")
    c.drawString(100, 660, f"Tanggal Pengembalian: {tanggal_kembali}")
    c.drawString(100, 645, f"Kode Tiket: {random_code}")

    # Menambahkan QR code ke PDF
    c.drawImage(qr_filename, 100, 500, width=1.5*inch, height=1.5*inch)
    
    # Menyelesaikan PDF
    c.showPage()
    c.save()
    
    print(f"Tiket peminjaman telah disimpan sebagai {pdf_filename}")

def kembalikan_buku(user_email, judul_buku):
    """Mengembalikan buku yang telah dipinjam dan memperbarui stok buku."""
    # Baca data buku dan data peminjaman
    data_buku = baca_data_buku()
    data_pinjam = baca_data_pinjam()
    buku_ketemu = False
    # Cari buku yang dikembalikan dan tambah stoknya
    for buku in data_buku:
        if buku["judul"] == judul_buku:
            buku_ketemu = True
            print("buku judul : ", buku["judul"])
            print("buku stok : ", buku["stok"])
            buku["stok"] = int(buku["stok"]) + 1
            # Hapus catatan peminjaman dari data_pinjam
            data_pinjam = [pinjam for pinjam in data_pinjam if not (pinjam["email"] == user_email and pinjam["judul"] == judul_buku)]

            # Simpan data buku yang telah diperbarui dan data peminjaman yang telah diperbarui
            simpan_data_buku(data_buku)
            simpan_data_pinjam(data_pinjam)

            print(f"Buku '{judul_buku}' berhasil dikembalikan.")
    if buku_ketemu == False:
        print(f"Buku '{judul_buku}' tidak ditemukan.")
def menuDua(user_email):
    while True:
        print("===   Beranda   ===")
        print("1. List Buku")
        print("2. Kategori")
        print("3. Cari Buku")
        print("4. Profil")
        print("5. Pengembalian Buku")
        print("6. Logout")
        menu = input("Menu pilihan (1/2/3/4/5/6): ")

        if menu == '1':
            data_buku = baca_data_buku()
            tampilkan_daftar_buku(data_buku)

            # Memilih buku
            buku_dipilih = pilih_buku(data_buku)

            # Menampilkan detail buku
            tampilkan_detail_buku(buku_dipilih)

            # Konfirmasi peminjaman
            konfirmasi = input("Apakah Anda ingin meminjam buku ini? (y/n): ")
            if konfirmasi.lower() == 'y':
                pinjam_buku(user_email, buku_dipilih)
                data_pinjam = baca_data_pinjam()
                data_peminjaman = next((d for d in data_pinjam if d["email"] == user_email and d["judul"] == buku_dipilih["judul"]), None)
                if data_peminjaman:
                    tanggal_pinjam = datetime.strptime(data_peminjaman["tanggalPinjam"], "%Y-%m-%d").date()
                    tanggal_kembali = datetime.strptime(data_peminjaman["tanggalKembali"], "%Y-%m-%d").date()
                    
                    # Cetak tiket peminjaman
                    create_loan_ticket(user_email, buku_dipilih['judul'], buku_dipilih['genre'], buku_dipilih['penulis'], tanggal_pinjam.strftime("%Y-%m-%d"), tanggal_kembali.strftime("%Y-%m-%d"))
                    
                    # Keluar dari loop menu utama setelah meminjam buku
                    break
            else:
                print("Peminjaman dibatalkan.")

        elif menu == '2':
            tampilkan_menu()
        elif menu == '3':
            cari_buku()
        elif menu == '4':
            print("Profil")
            tampilkan_profil(str(user_email))
        elif menu == '5':
            judul_buku = input("Masukkan judul buku yang ingin dikembalikan: ")
            kembalikan_buku(user_email, judul_buku)
        elif menu == '6':
            print("Logout berhasil.")
            break
        else:
            print("Menu tidak valid, silahkan input kembali!")