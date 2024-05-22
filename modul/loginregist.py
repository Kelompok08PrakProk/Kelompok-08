import csv
import random
import smtplib
from email.message import EmailMessage
import pandas as pd

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
                print(f"Sinopsis: {row['sinopsis']}\n")
                
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



def tampilkan_profil(user_email, file_path='database/databaseUser.csv'):
    try:
        # Pastikan user_email adalah string dan bukan boolean
        if not isinstance(user_email, str):
            print("Email tidak valid.")
            return
        
        # Membaca file CSV
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Mencari data pengguna berdasarkan email
        user_data = df[df['email'].str.lower() == user_email.lower()]
        
        if user_data.empty:
            print("Data pengguna tidak ditemukan.")
        else:
            user_info = user_data.iloc[0]
            print(f"Nama Lengkap: {user_info['namalengkap']}")
            print(f"Alamat: {user_info['alamat']}")
            print(f"Nomor HP: {user_info['nomorHP']}")
                
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def menuDua(user_email):
    while True:
        print("===   Beranda   ===")
        print("1. List Buku")
        print("2. Kategori")
        print("3. Cari Buku")
        print("4. Profil")
        print("5. Logout")
        menu = input("Menu pilihan (1/2/3/4/5): ")

        if menu == '1':
            tampilkan_daftar_buku()
        elif menu == '2':
            tampilkan_menu()
        elif menu == '3':
            cari_buku()
            # Tambahkan fungsi untuk mencari buku di sini
        elif menu == '4':
            print("Profil")
            tampilkan_profil(str(user_email))
            # Tambahkan fungsi untuk profil di sini
        elif menu == '5':
            print("Logout berhasil.")
            break
        else:
            print("Menu tidak valid, silahkan input kembali!")
