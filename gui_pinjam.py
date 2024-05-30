import os
from customtkinter import *
import customtkinter as ctk
from tkinter import Text, messagebox
from PIL import Image

# Global variable to keep track of stock
book_stock = 10

def show_book_details(buku_dipilih):
    for idx, row in df.iterrows():
        book_image_path = row['cover']
        
        if os.path.exists(book_image_path):
            try:
                book_img = Image.open(book_image_path)
                resize_img = novel_image.resize((350, 450))
                book_image = ImageTk.PhotoImage(resize_img)
            except Exception as e:
                print(f"Error loading image {book_image_path}: {e}")
                book_image = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="red"))
        else:
            print(f"Book image not found: {book_image_path}")
            book_image = ImageTk.PhotoImage(Image.new("RGB", (300, 450), color="gray")) 
    
    novel_img_label = ctk.CTkLabel(window_beranda, image=book_image, text="")
    novel_img_label.place(relx=0.25, rely=0.5, anchor="center")
    
    book_desc_frame = ctk.CTkFrame(window_beranda, width=600, height=400, bg='#1A1F23', fg='#E3DFE6', font=("Trebuchet MS", 16), border_width=0)
    book_desc_frame.place(relx=0.51, rely=0.6, anchor="center")
    
    label_judul = ctk.CTkLabel(detail_window, text=f"Judul: {buku_dipilih['judul']}", font=("Arial", 12))
    label_judul.pack()
    
    label_genre = ctk.CTkLabel(detail_window, text=f"Genre: {buku_dipilih['genre']}", font=("Arial", 12))
    label_genre.pack()
    
    label_penulis = ctk.CTkLabel(detail_window, text=f"Penulis: {buku_dipilih['penulis']}", font=("Arial", 12))
    label_penulis.pack()
    
    label_tahun = ctk.CTkLabel(detail_window, text=f"Tahun Terbit: {buku_dipilih['tahunTerbit']}", font=("Arial", 12))
    label_tahun.pack()
    
    label_halaman = ctk.CTkLabel(detail_window, text=f"Halaman: {buku_dipilih['halaman']}", font=("Arial", 12))
    label_halaman.pack()
    
    label_sinopsis = ctk.CTkLabel(detail_window, text=f"Sinopsis: {buku_dipilih['sinopsis']}", font=("Arial", 12))
    label_sinopsis.pack()
    
    label_stok = ctk.CTkLabel(detail_window, text=f"Stok: {buku_dipilih['stok']}", font=("Arial", 12))
    label_stok.pack()

    button_back = ctk.CTkButton(window_beranda, width=100, height=35, corner_radius=0, fg_color="#1A1F23", border_width=0, text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=False, command=back_to_home)
    button_back.place(relx=0.08, rely=0.16, anchor="w")
    
    global stock_button
    stock_button = ctk.CTkButton(window_beranda, text=f"Stok : {book_stock}", width=50, height=25, corner_radius=30, fg_color="#A84F6C", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16))
    stock_button.place(relx=0.39, rely=0.7, anchor="center")
    
    borrow_button = ctk.CTkButton(window_beranda, text="PINJAM", width=120, height=35, corner_radius=30, fg_color="transparent", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16), command=borrow_book)
    borrow_button.place(relx=0.4, rely=0.8, anchor="center")
    
        
def borrow_book():
    global book_stock
    if book_stock > 0:
        book_stock -= 1
        stock_button.configure(text=f"Stok : {book_stock}")
        if book_stock == 0:
            messagebox.showinfo("Info", "Maaf, stok buku habis")
    else:
        messagebox.showinfo("Info", "Maaf, stok buku habis")

def back_to_home():
    for widget in window_beranda.winfo_children():
        widget.destroy()
    setup_home_screen()

def setup_home_screen():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo2_path = os.path.join(script_dir, "gambar/logo2.png")
    icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
    icon_acc_path = os.path.join(script_dir, "gambar/account_icon.png")

    try:
        logo2 = Image.open(logo2_path)
        resize_img = logo2.resize((320,117))
        logo2 = ctk.CTkImage(resize_img)
        icon_search = Image.open(icon_search_path)
        resize_img = icon_search.resize((30,30))
        icon_search = ctk.CTkImage(resize_img)
        icon_acc = Image.open(icon_acc_path)
        resize_img = icon_acc.resize((70,70))
        icon_acc = ctk.CTkImage(resize_img)
    except FileNotFoundError as e:
        messagebox.showerror("File Not Found", f"Error: {e}")
        return

    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="")
    l1.pack(pady=0, anchor="nw")

    button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
    button1.place(relx=0.5, rely=0.055, anchor="center")

    button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
    button2.place(relx=0.63, rely=0.055, anchor="center")

    entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", border_width=0, text_color="#1A1F23", placeholder_text="Search", font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
    entry1.place(relx=0.81, rely=0.055, anchor="center")

    button3 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_search, corner_radius=0, bg_color="#9C909D", fg_color="#9C909D", border_width=0, text="", hover=False)
    button3.place(relx=0.867, rely=0.055, anchor="center")

    button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
    button4.place(relx=0.95, rely=0.055, anchor="center")

    show_book_details(buku_dipilih)

window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x800")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True, True)

setup_home_screen()

window_beranda.mainloop()
