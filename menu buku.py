import customtkinter as ctk
from PIL import Image, ImageTk

# Initialize the customtkinter app
app = ctk.CTk()
app.geometry("800x600")
app.title("Peti Dependable Library")

# Configure the grid layout
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Top Navigation Bar
top_nav_frame = ctk.CTkFrame(app)
top_nav_frame.grid(row=0, column=0, sticky="nsew")
top_nav_frame.grid_rowconfigure(0, weight=1)
top_nav_frame.grid_columnconfigure(0, weight=1)
top_nav_frame.grid_columnconfigure(1, weight=1)
top_nav_frame.grid_columnconfigure(2, weight=1)
top_nav_frame.grid_columnconfigure(3, weight=1)

btn_beranda = ctk.CTkButton(top_nav_frame, text="Beranda")
btn_beranda.grid(row=0, column=0, padx=20, pady=10)

btn_kategori = ctk.CTkButton(top_nav_frame, text="Kategori")
btn_kategori.grid(row=0, column=1, padx=20, pady=10)

entry_cari = ctk.CTkEntry(top_nav_frame, placeholder_text="Cari")
entry_cari.grid(row=0, column=2, padx=20, pady=10)

btn_user = ctk.CTkButton(top_nav_frame, text="User")
btn_user.grid(row=0, column=3, padx=20, pady=10)

# Main Content Frame
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, sticky="nsew")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Book Information
book_info_frame = ctk.CTkFrame(main_frame)
book_info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

title_label = ctk.CTkLabel(book_info_frame, text="Novel\nLaut Bercerita\nLeila S. Chudori", font=ctk.CTkFont(size=20, weight="bold"))
title_label.grid(row=0, column=0, padx=10, pady=10)

details_label = ctk.CTkLabel(book_info_frame, text="Tahun terbit: 2017\nJumlah halaman: 379 halaman")
details_label.grid(row=1, column=0, padx=10, pady=10)

synopsis_label = ctk.CTkLabel(book_info_frame, text="Sinopsis: Laut Bercerita, novel terbaru Leila S. Chudori, bertutur tentang kisah keluarga yang kehilangan, sekumpulan sahabat yang merasakan kekosongan di dada, sekelompok orang yang gemar menyiksa dan lancar berkhianat, sejumlah keluarga yang mencari kejelasan makam anaknya, dan tentang cinta yang tak akan luntur.")
synopsis_label.grid(row=2, column=0, padx=10, pady=10)

stock_label = ctk.CTkLabel(book_info_frame, text="Stok: 10", font=ctk.CTkFont(size=16, weight="bold"))
stock_label.grid(row=3, column=0, padx=10, pady=10)

btn_pinjam = ctk.CTkButton(book_info_frame, text="PINJAM", fg_color="red", text_color="white")
btn_pinjam.grid(row=4, column=0, padx=10, pady=20)

# Book Cover Image
image_frame = ctk.CTkFrame(main_frame)
image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Run the app
app.mainloop()
