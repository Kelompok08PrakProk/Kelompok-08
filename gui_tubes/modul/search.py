import pandas as pd

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

def tampilkan_daftar_buku(file_path):
    try:
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Memeriksa apakah kolom 'Judul' ada dalam DataFrame
        if 'judul' not in df.columns:
            print("Kolom 'Judul' tidak ditemukan dalam file CSV.")
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

# Contoh penggunaan fungsi dengan path lengkap
tampilkan_daftar_buku('database/databuku.csv')
