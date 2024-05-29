import os
from customtkinter import *
import customtkinter as ctk
from tkinter import Text
from PIL import Image, ImageTk

def show_novel_details(novel_image_path, novel_description):
    try:
        novel_image = Image.open(novel_image_path)
        resize_novel_img = novel_image.resize((350, 450))
        novel_image = ImageTk.PhotoImage(resize_novel_img)
        
        novel_img_label = ctk.CTkLabel(window_beranda, image=novel_image, text="", bg_color="transparent", fg_color="transparent")
        novel_img_label.image = novel_image  
        novel_img_label.place(relx=0.25, rely=0.5, anchor="center")
        
        novel_desc_text = Text(window_beranda, wrap='word', bg='#1A1F23', fg='#E3DFE6', font=("Trebuchet MS", 16), borderwidth=0, highlightthickness=0)
        novel_desc_text.insert("1.0", novel_description)
        novel_desc_text.tag_add("justify", "1.0", "end")
        novel_desc_text.tag_configure("justify", justify="left")
        novel_desc_text.place(relx=0.51, rely=0.6, anchor="center", width=600, height=400)
        novel_desc_text.configure(state="disabled")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        back_arrow_path = os.path.join(script_dir, "gambar/back_arrow.png")
        back_arrow = Image.open(back_arrow_path)
        resize_arrow_img = back_arrow.resize((200, 25))
        back_arrow = ImageTk.PhotoImage(resize_arrow_img)

        back_button = ctk.CTkButton(window_beranda, image=back_arrow, text="Kembali", width=40, height=40, corner_radius=30, fg_color="transparent" , command=back_to_home)
        back_button.image = back_arrow  
        back_button.place(relx=0.05, rely=0.11, anchor="nw")

        stock_button = ctk.CTkButton(window_beranda, text="Stok : 10", width=50, height=25, corner_radius=30, fg_color="#A84F6C", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16))
        stock_button.place(relx=0.39, rely=0.7, anchor="center")
        
        borrow_button = ctk.CTkButton(window_beranda, text="PINJAM", width=120, height=35, corner_radius=30, fg_color="transparent", border_width=1, border_color="#A84F6C", text_color="#E3DFE6", font=("Trebuchet MS", 16))
        borrow_button.place(relx=0.4, rely=0.8, anchor="center")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")

def back_to_home():
    for widget in window_beranda.winfo_children():
        widget.destroy()
    setup_home_screen()

def setup_home_screen():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo2_path = os.path.join(script_dir, "gambar/logo2.png")
    icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
    icon_acc_path = os.path.join(script_dir, "gambar/account_icon.png")

    logo2 = Image.open(logo2_path)
    resize_img = logo2.resize((320,117))
    logo2 = ImageTk.PhotoImage(resize_img)
    icon_search = Image.open(icon_search_path)
    resize_img = icon_search.resize((30,30))
    icon_search = ImageTk.PhotoImage(resize_img)
    icon_acc = Image.open(icon_acc_path)
    resize_img = icon_acc.resize((70,70))
    icon_acc = ImageTk.PhotoImage(resize_img)

    l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
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

    show_novel_details(os.path.join(script_dir, "gambar/cover buku/Novel/1.jpg"), 
                       "Tahun Terbit: 2017\nJumlah Halaman: 379\n\nSinopsis : Laut Bercerita, novel terbaru Leila S. Chudori, bertutur tentang kisah keluarga yang kehilangan, sekumpulan sahabat yang merasakan kekosongan di dada, sekelompok orang yang gemar menyiksa dan lancar berkhianat, sejumlah keluarga yang mencari kejelasan makam anaknya, dan tentang cinta yang tak akan luntur.")

window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x800")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True,True)

setup_home_screen()

window_beranda.mainloop()
