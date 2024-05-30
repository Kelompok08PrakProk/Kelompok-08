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
detail_buku_frame = None

def kembali(last_button=None):
    detail_buku_frame.pack_forget()
    main_frame.pack(side=ctk.TOP, fill="both", expand=True)  # Menampilkan kembali frame utama
    category_frame.pack_forget()  # Pastikan frame kategori tidak ditampilkan
    if last_button == "kategori":
        detail_buku_frame.pack_forget()
        category_frame
    else:
        detail_buku_frame.pack_forget()
        main_frame

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
        
        book_desc_frame = ctk.CTkFrame(detail_buku_frame, width=400, height=400, bg_color="#1A1F23", fg_color="#1A1F23")
        book_desc_frame.place(relx=0.58, rely=0.7  , anchor="center")

        label_genre = ctk.CTkLabel(book_desc_frame, text=f"Genre: {buku_dipilih['genre']}", font=("Trebuchet MS", 16))
        label_genre.pack(side="top", anchor="w", pady=1, padx=10)

        label_judul = ctk.CTkLabel(book_desc_frame, text=f"Judul: {buku_dipilih['judul']}", font=("Trebuchet MS", 20))
        label_judul.pack(side="top", anchor="w", pady=1, padx=10)

        label_penulis = ctk.CTkLabel(book_desc_frame, text=f"Penulis: {buku_dipilih['penulis']}", font=("Trebuchet MS", 12))
        label_penulis.pack(side="top", anchor="w", pady=1, padx=10)

        label_tahun = ctk.CTkLabel(book_desc_frame, text=f"Tahun Terbit: {buku_dipilih['tahunTerbit']}", font=("Trebuchet MS", 12))
        label_tahun.pack(side="top", anchor="w", pady=5, padx=10)

        label_halaman = ctk.CTkLabel(book_desc_frame, text=f"Halaman: {buku_dipilih['halaman']}", font=("Trebuchet MS", 12))
        label_halaman.pack(side="top", anchor="w", pady=5, padx=10)

        label_sinopsis = ctk.CTkLabel(book_desc_frame, text=f"Sinopsis: {buku_dipilih['sinopsis']}", font=("Trebuchet MS", 12), wraplength=800)
        label_sinopsis.configure(justify="left")
        label_sinopsis.pack(side="top", anchor="w", pady=5, padx=10)
    
        label_stok = ctk.CTkLabel(book_desc_frame, text=f"Stok: {buku_dipilih['stok']}", font=("Trebuchet MS", 16))
        label_stok.pack(side="top", anchor="w", pady=5, padx=10)

        button_back = ctk.CTkButton(detail_buku_frame, width=100, height=35, corner_radius=30, fg_color="#1A1F23", border_width=0, text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=False, command=kembali)
        button_back.place(relx=0.1, rely=0.1, anchor="e")

        borrow_button = ctk.CTkButton(detail_buku_frame, text="PINJAM", width=120, height=35, corner_radius=30, fg_color="#A84F6C", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16))
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
                        hover=False)
    button3.place(relx=0.88, rely=0.055, anchor="center")

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
