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


# Fungsi untuk menampilkan daftar buku
def tampilkan_daftar_buku(scrollable_frame, file_path='database/databuku.csv'):
    try:
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, encoding="windows-1252")
        
        # Memeriksa apakah kolom 'judul' ada dalam DataFrame
        if 'judul' not in df.columns:
            print("Kolom 'judul' tidak ditemukan dalam file CSV.")
            return
        
        # Load cover buku dari direktori coverbuku
        cover_dir = os.path.join(script_dir, 'coverbuku')
        
        # Menampilkan daftar buku
        for idx, row in df.iterrows():
            cover_path = os.path.join(cover_dir, f"{row['judul']}.jpg")
            
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

            label_cover = ctk.CTkLabel(frame_buku, image=cover_photo, text="", fg_color="transparent")
            label_cover.image = cover_photo  # Menyimpan referensi gambar
            label_cover.pack(side="top")

            label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6")
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
        
        # Filter buku berdasarkan genre
        buku_genre = df[df['genre'].str.lower() == genre.lower()]
        
        if buku_genre.empty:
            print(f"Tidak ada buku dengan genre '{genre}' yang ditemukan.")
            return
        
        # Load cover buku dari direktori coverbuku
        cover_dir = os.path.join(script_dir, 'coverbuku')
        
        # Menghapus widget lama dari scrollable_frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Menampilkan daftar buku berdasarkan genre
        for idx, row in buku_genre.iterrows():
            cover_path = os.path.join(cover_dir, f"{row['judul']}.jpg")
            
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

            frame_buku = ctk.CTkFrame(category_scrollable_frame, width=360, height=600, fg_color="#1A1F23")
            frame_buku.pack(side="left", padx=10, pady=10)

            label_cover = ctk.CTkLabel(frame_buku, image=cover_photo, text="", fg_color="transparent")
            label_cover.image = cover_photo  # Menyimpan referensi gambar
            label_cover.pack(side="top")

            label_judul = ctk.CTkLabel(frame_buku, text=row['judul'], fg_color="transparent", text_color="#E3DFE6")
            label_judul.pack(side="top")
    
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print(f"File '{file_path}' kosong atau tidak dapat dibaca.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x600")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True,True)

script_dir = os.path.dirname(os.path.abspath(__file__))
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
    option_menu = ctk.CTkOptionMenu(category_frame, values=["Novel", "Cerpen", "Biografi", "Komik", "Ensiklopedia", "Kamus", "Majalah"], 
                                    width=170, height=26, fg_color="#A6A4A8", button_color="#A6A4A8", button_hover_color="#E3DFE6",
                                    text_color="#1A1F23", corner_radius=30, command=lambda genre: tampilkan_buku_berdasarkan_genre(category_scrollable_frame, genre))
    option_menu.place(relx=0.1, rely=0.02, anchor="n")

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


l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
l1.place(x=10, y=10, anchor="nw")

entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", border_width=0, text_color="#1A1F23", placeholder_text="Search", font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
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

button3 = ctk.CTkButton(window_beranda, width=20, height=20, image=icon_search, corner_radius=0, bg_color="#9C909D", 
                        fg_color="#9C909D", border_width=0, text="", hover=False)
button3.place(relx=0.88, rely=0.055, anchor="center")

button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", 
                        fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
button4.place(relx=0.95, rely=0.055, anchor="center")

scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=1200, height=500, fg_color="#1A1F23", orientation="horizontal")
scrollable_frame.pack(side="top", fill="both", expand=True)

category_scrollable_frame = ctk.CTkScrollableFrame(category_frame, width=1200, height=500, fg_color="#1A1F23", orientation="horizontal")
category_scrollable_frame.pack(side="top", fill="both", expand=True)

# Tampilkan daftar buku di scrollable frame
show_beranda()


window_beranda.mainloop()