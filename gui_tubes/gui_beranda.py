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


window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x800")
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

window_beranda.mainloop()