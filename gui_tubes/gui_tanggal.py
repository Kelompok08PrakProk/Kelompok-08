import customtkinter as ctk
from PIL import Image, ImageTk
import os
from tkcalendar import Calendar  # Pastikan Anda sudah menginstall tkcalendar dengan 'pip install tkcalendar'
from datetime import datetime, timedelta
import datetime

def kembali():
    # Contoh tindakan ketika tombol kembali ditekan
    print("Tombol Kembali ditekan")
    window_beranda.destroy()

def show_calendar(button):
    calendar_window = ctk.CTkToplevel(frame_tanggal_pinjam)
    calendar_window.geometry("300x300")
    calendar = Calendar(calendar_window, selectmode='day', date_pattern='dd-mm-yyyy')
    calendar.pack(pady=10)

    def get_date():
        selected_date = calendar.get_date()
        select_button.configure(text=selected_date)
        button_tampilkan_pinjam.configure(text=selected_date)
        
        # Hitung tanggal pengembalian
        tanggal_peminjaman = datetime.strptime(selected_date, "%d-%m-%Y")
        tanggal_pengembalian = tanggal_peminjaman + timedelta(days=7)
        label_tanggal_kembali.configure(text=tanggal_pengembalian.strftime("%Y-%m-%d"))


        calendar_window.destroy()

    select_button = ctk.CTkButton(calendar_window, text="Select Date", command=get_date)
    select_button.pack(pady=10)


# Angkat jendela kalender ke depan
    calendar_window.lift()

    # Jadikan jendela kalender sebagai jendela utama sementara
    calendar_window.grab_set()

# Membuat jendela utama
window_beranda = ctk.CTk()
window_beranda.title("Beranda")
window_beranda.geometry("1300x800")
window_beranda.configure(fg_color="#1A1F23")
window_beranda.resizable(True, True) 

# Mendapatkan direktori skrip
script_dir = os.path.dirname(os.path.abspath(__file__))
logo2_path = os.path.join(script_dir, "gambar/logo2.png")
icon_search_path = os.path.join(script_dir, "gambar/search_icon.png")
icon_acc_path = os.path.join(script_dir, "gambar/account_icon.png")
cover_buku_path = os.path.join(script_dir, "gambar/cover buku/Novel/1.jpg")  # Path ke gambar sampul buku
background_cover_path = os.path.join(script_dir, "gambar/Background/Novel/Laut Bercerita.jpg")

# Memuat dan mengubah ukuran gambar logo
logo2 = ctk.CTkImage(light_image=Image.open(logo2_path), size=(320, 117))
icon_search = ctk.CTkImage(light_image=Image.open(icon_search_path), size=(20, 20))
icon_acc = ctk.CTkImage(light_image=Image.open(icon_acc_path), size=(70, 70))
cover_buku = ctk.CTkImage(light_image=Image.open(cover_buku_path), size=(200, 300))
background_cover= ctk.CTkImage(light_image=Image.open(background_cover_path), size=(1850,200))

# Memuat gambar sampul buku
cover_buku = ctk.CTkImage(light_image=Image.open(cover_buku_path), size=(250, 350))

# Membuat label untuk logo
l1 = ctk.CTkLabel(window_beranda, image=logo2, text="", bg_color="transparent", fg_color="transparent")
l1.pack(pady=0, anchor="nw")

# Background covernya
background_cover = ctk.CTkLabel(window_beranda, image=background_cover, text="", bg_color="transparent", fg_color="transparent")
background_cover.place(relx=0.5, rely=0.36, anchor="center")

# Membuat tombol "Beranda"
button1 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Beranda", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
button1.place(relx=0.5, rely=0.055, anchor="center")

# Membuat tombol "Kategori"
button2 = ctk.CTkButton(window_beranda, width=120, height=35, corner_radius=30, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="Kategori", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C")
button2.place(relx=0.63, rely=0.055, anchor="center")

# Membuat entry untuk pencarian
entry1 = ctk.CTkEntry(window_beranda, width=220, height=35, corner_radius=30, fg_color="#9C909D", border_width=0, text_color="#1A1F23", placeholder_text="Search", font=('Trebuchet MS', 16), placeholder_text_color="#E3DFE6")
entry1.place(relx=0.81, rely=0.055, anchor="center")

# Membuat tombol pencarian
button3 = ctk.CTkButton(window_beranda, width=30, height=30, image=icon_search, corner_radius=0, bg_color="#9C909D", fg_color="#9C909D", border_width=0, text="", hover=False)
button3.place(relx=0.867, rely=0.055, anchor="center")

# Membuat tombol akun
button4 = ctk.CTkButton(window_beranda, width=70, height=70, image=icon_acc, corner_radius=0, bg_color="#1A1F23", fg_color="#1A1F23", border_width=0, text="", hover=True, hover_color="#232A30")
button4.place(relx=0.95, rely=0.055, anchor="center")

# Membuat tombol "Kembali"
button_back = ctk.CTkButton(window_beranda, width=100, height=35, corner_radius=0, fg_color="#1A1F23", border_width=0, border_color="#A84F6C", text="← Kembali", text_color="#E3DFE6", font=("Trebuchet MS", 16), hover=True, hover_color="#A84F6C", command=kembali)
button_back.place(relx=0.08, rely=0.15, anchor="w")

frame_tanggal_pinjam = ctk.CTkFrame(window_beranda, width=500, height=60, corner_radius=10, fg_color="#e3dfe6")
frame_tanggal_pinjam.place(relx=0.3, rely=0.55, anchor="center")

# Membuat tombol "Tanggal Peminjaman"
button_tanggal_pinjam = ctk.CTkButton(window_beranda, width=250, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, border_color="#a6a4a8", text="Tanggal Peminjaman", text_color="#000000", font=("Trebuchet MS", 16), hover=True, hover_color="#AAAAAA")
button_tanggal_pinjam.place(relx=0.23, rely=0.55, anchor="center")
button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))  # Adjusted here

# Tombol untuk menampilkan tanggal yang telah dipilih
button_tampilkan_pinjam = ctk.CTkButton(window_beranda, width=150, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, border_color="#e3dfe6", text="", text_color="#000000", font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
button_tampilkan_pinjam.place(relx=0.4, rely=0.55, anchor="center")
button_tanggal_pinjam.configure(command=lambda: show_calendar(button_tanggal_pinjam))


frame_tanggal_kembali = ctk.CTkFrame(window_beranda, width=500, height=60, corner_radius=10, fg_color="#e3dfe6")
frame_tanggal_kembali.place(relx=0.3, rely=0.65, anchor="center")

# Membuat tombol "Tanggal Pengembalian"
button_tanggal_kembali = ctk.CTkButton(window_beranda, width=250, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#a6a4a8", border_width=1, border_color="#a6a4a8", text="Tanggal Pengembalian", text_color="#000000", font=("Trebuchet MS", 16), hover=True, hover_color="#AAAAAA")
button_tanggal_kembali.place(relx=0.23, rely=0.65, anchor="center")
button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))  # Adjusted here

# Tombol untuk menampilkan tanggal yang telah dipilih
button_tampilkan_kembali = ctk.CTkButton(window_beranda, width=150, height=40, corner_radius=10, bg_color= "#e3dfe6", fg_color="#e3dfe6", border_width=1, border_color="#e3dfe6", text="", text_color="#000000", font=("Trebuchet MS", 12), hover=False, hover_color="#AAAAAA")
button_tampilkan_kembali.place(relx=0.4, rely=0.65, anchor="center")
button_tanggal_kembali.configure(command=lambda: show_calendar(button_tanggal_kembali))

# Membuat label untuk menampilkan tanggal pengembalian
label_tanggal_kembali = ctk.CTkLabel(window_beranda, text="", font=("Trebuchet MS", 16), bg_color="#e3dfe6", fg_color="#000000")
label_tanggal_kembali.place(relx=0.6, rely=0.55, anchor="center")


# Membuat tombol "Cetak"
button_cetak = ctk.CTkButton(window_beranda, width=200, height=50, corner_radius=10, fg_color="#1A1F23", border_width=1, border_color="#A84F6C", text="CETAK", text_color="#E3DFE6", font=("Trebuchet MS", 20), hover=True, hover_color="#A84F6C")
button_cetak.place(relx=0.3, rely=0.8, anchor="center")

# Menampilkan gambar sampul buku
cover_buku_label = ctk.CTkLabel(window_beranda, image=cover_buku, text="", bg_color="transparent", fg_color="transparent")
cover_buku_label.place(relx=0.69, rely=0.5, anchor="center")

# Menambahkan judul buku
judul_buku_label = ctk.CTkLabel(window_beranda, text="Laut Bercerita", font=("Trebuchet MS", 30), text_color="#E3DFE6", bg_color="transparent", fg_color="transparent", padx=0, pady=0)
judul_buku_label.place(relx=0.69, rely=0.8, anchor="center")

window_beranda.mainloop()