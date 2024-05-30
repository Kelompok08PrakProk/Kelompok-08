from customtkinter import *
import customtkinter as ctk
from tkinter import Text
from PIL import Image, ImageTk
import os
import random
import smtplib
import csv
import pandas as pd
from email.message import EmailMessage
from loginregist import register_user, login_user, menuDua

script_dir = os.path.dirname(os.path.abspath(__file__))

def tampilkan_detail_buku(buku_dipilih, df):
    try:
        if 'cover' not in df.columns:
            print("Kolom 'cover' tidak ditemukan dalam file CSV.")
            return
        
        cover_path = buku_dipilih['cover']
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
    

        novel_img_frame = ctk.CTkFrame(window_beranda, width=350, height=450, fg_color="red")
        novel_img_frame.place(relx=0.4, rely=0.5, anchor="e")

        novel_img_label = ctk.CTkLabel(novel_img_frame, image=cover_photo, text="")
        novel_img_label.place(relx=0.5, rely=0.5, anchor="center")
        
        book_desc_frame = ctk.CTkFrame(window_beranda, width=800, height=600, bg_color="#1A1F23", fg_color="green")
        book_desc_frame.place(relx=0.7, rely=0.6, anchor="center")

        label_judul = ctk.CTkLabel(book_desc_frame, text=f"Judul: {buku_dipilih['judul']}", font=("Arial", 12), wrapline=300)
        label_judul.configure("justify", justify="left")
        label_judul.pack(pady=5)
        
        label_genre = ctk.CTkLabel(book_desc_frame, text=f"Genre: {buku_dipilih['genre']}", font=("Arial", 12), wrapline=300)
        label_genre.configure("justify", justify="left")
        label_genre.pack(pady=5)
        
        label_penulis = ctk.CTkLabel(book_desc_frame, text=f"Penulis: {buku_dipilih['penulis']}", font=("Arial", 12), wrapline=300)
        label_penulis.configure("justify", justify="left")
        label_penulis.pack(pady=5)
        
        label_tahun = ctk.CTkLabel(book_desc_frame, text=f"Tahun Terbit: {buku_dipilih['tahunTerbit']}", font=("Arial", 12), wrapline=300)
        label_tahun.configure("justify", justify="left")
        label_tahun.pack(pady=5)
        
        label_halaman = ctk.CTkLabel(book_desc_frame, text=f"Halaman: {buku_dipilih['halaman']}", font=("Arial", 12), wrapline=300)
        label_halaman.configure("justify", justify="left")
        label_halaman.pack(pady=5)
        
        label_sinopsis = ctk.CTkLabel(book_desc_frame, text=f"Sinopsis: {buku_dipilih['sinopsis']}", font=("Arial", 12), wrapline=300)
        label_sinopsis.configure("justify", justify="left")
        label_sinopsis.pack(pady=5)
        
        label_stok = ctk.CTkLabel(book_desc_frame, text=f"Stok: {buku_dipilih['stok']}", font=("Arial", 12))
        label_stok.configure("justify", justify="left")
        label_stok.pack(pady=5)

        button_back = ctk.CTkButton(window_beranda, width=100, height=35, corner_radius=0, fg_color="#1A1F23", border_width=0, text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=False, command=back_to_home)
        button_back.place(relx=0.08, rely=0.16, anchor="w")
        
        global stock_button
        stock_button = ctk.CTkButton(window_beranda, text=f"Stok : {stok}", width=50, height=25, corner_radius=30, fg_color="#A84F6C", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16), state=DISABLED)
        stock_button.place(relx=0.39, rely=0.7, anchor="w")
        
        borrow_button = ctk.CTkButton(window_beranda, text="PINJAM", width=120, height=35, corner_radius=30, fg_color="transparent", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16), command=pinjam_buku)
        borrow_button.place(relx=0.4, rely=0.8, anchor="w")
        
    except FileNotFoundError as e:
        messagebox.showerror("File Not Found", f"Error: {e}")

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
            button_cover = ctk.CTkButton(frame_buku, image=cover_photo, text="", fg_color="transparent", command=lambda buku=row: tampilkan_detail_buku(buku, df))
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
                            fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30", command=show_account_frame)
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
window_beranda.geometry("1300x600")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True,True)

# Tampilkan daftar buku di scrollable frame
setup_home_screen()

window_beranda.mainloop()
