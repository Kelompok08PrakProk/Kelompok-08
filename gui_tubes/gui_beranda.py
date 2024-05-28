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
    # Reset all indicators
    button1_indicate.configure(fg_color="#1A1F23")
    button2_indicate.configure(fg_color="#1A1F23")
    # Highlight the selected indicator
    label.configure(fg_color="#A84F6C")

option_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")

option_frame.pack(side=ctk.TOP)
option_frame.pack_propagate(False)
option_frame.configure(width=1300, height=120)

menu_frame = ctk.CTkFrame(window_beranda, fg_color="#1A1F23")

option_frame.pack(side=ctk.TOP)
option_frame.pack_propagate(False)
option_frame.configure(width=1300, height=600)


l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
l1.place(x=10, y=10, anchor="nw")

entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", border_width=0, text_color="#1A1F23", placeholder_text="Search", font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
entry1.place(relx=0.81, rely=0.055, anchor="center")

button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                        text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                        hover_color="#232A30", command=lambda:indicate(button1_indicate))
button1.place(relx=0.5, rely=0.055, anchor="center")

button1_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", fg_color="#1A1F23")
button1_indicate.place(relx=0.5, rely=0.08, anchor="center")

button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=0, fg_color="#1A1F23", 
                        text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, 
                        hover_color="#232A30", command=lambda:indicate(button2_indicate))
button2.place(relx=0.63, rely=0.055, anchor="center")

button2_indicate = ctk.CTkLabel(option_frame, width=120, height=1, corner_radius=30, text="", bg_color="#1A1F23", fg_color="#1A1F23")
button2_indicate.place(relx=0.63, rely=0.08, anchor="center")

button3 = ctk.CTkButton(window_beranda, width=20, height=20, image=icon_search, corner_radius=0, bg_color="#9C909D", 
                        fg_color="#9C909D", border_width=0, text="", hover=False)
button3.place(relx=0.88, rely=0.055, anchor="center")

button4 = ctk.CTkButton(window_beranda, width=6, height=6, image=icon_acc, corner_radius=0, bg_color="#1A1F23", 
                        fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
button4.place(relx=0.95, rely=0.055, anchor="center")


window_beranda.mainloop()