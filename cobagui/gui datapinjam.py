import customtkinter as ctk
import pandas as pd

user_email = "dimasadira45@gmail.com"


# Fungsi untuk membaca data buku dari CSV
def baca_data_buku():
    try:
        return pd.read_csv('database/databuku.csv').to_dict('records')
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data buku ke CSV
def simpan_data_buku(data_buku):
    df = pd.DataFrame(data_buku)
    df.to_csv('database/databuku.csv', index=False)

# Fungsi untuk membaca data pinjaman dari CSV
def baca_data_pinjam():
    try:
        return pd.read_csv('database/datapinjam.csv').to_dict('records')
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data pinjaman ke CSV
def simpan_data_pinjam(data_pinjam):
    df = pd.DataFrame(data_pinjam)
    df.to_csv('database/datapinjam.csv', index=False)

# Fungsi untuk mengembalikan buku yang dipinjam
def kembalikan_buku(user_email, judul_buku):
    data_buku = baca_data_buku()
    data_pinjam = baca_data_pinjam()
    buku_ketemu = False
    
    for buku in data_buku:
        if buku["judul"] == judul_buku:
            buku_ketemu = True
            buku["stok"] = int(buku["stok"]) + 1
            data_pinjam = [pinjam for pinjam in data_pinjam if not (pinjam["email"] == user_email and pinjam["judul"] == judul_buku)]

            simpan_data_buku(data_buku)
            simpan_data_pinjam(data_pinjam)

            print(f"Buku '{judul_buku}' berhasil dikembalikan.")
            display_data(user_email)  # Update display after returning a book
            return
    
    if not buku_ketemu:
        print(f"Buku '{judul_buku}' tidak ditemukan.")
        ctk.CTkLabel(frame_return, text=f"Buku '{judul_buku}' tidak ditemukan.", fg_color="red").pack()

# Fungsi untuk menampilkan data peminjaman berdasarkan email
def display_data(email):
    data = baca_data_pinjam()
    user_data = [pinjam for pinjam in data if pinjam['email'] == email]

    for widget in frame_data.winfo_children():
        widget.destroy()
    
    if user_data:
        for row in user_data:
            frame_entry = ctk.CTkFrame(frame_data)
            frame_entry.pack(pady=5, padx=5, fill='x')
            
            ctk.CTkLabel(frame_entry, text=f"Judul: {row['judul']} | Tanggal Pinjam: {row['tanggalPinjam']} | Tanggal Kembali: {row['tanggalKembali']}").pack(side='left')
            ctk.CTkButton(frame_entry, text="Kembalikan", command=lambda r=row: kembalikan_buku(email, r['judul'])).pack(side='right')
    else:
        ctk.CTkLabel(frame_data, text="No records found").pack(anchor='w')

# Fungsi untuk mencari data berdasarkan email
def search():
    display_data(user_email)

# Setup GUI
app = ctk.CTk()
app.geometry("600x500")
app.title("Buku Saya")

# Frame untuk input email dan mencari data peminjaman
frame_input = ctk.CTkFrame(app)
frame_input.pack(pady=10)

ctk.CTkLabel(frame_input, text=f"Loan records for user: {user_email}").pack(anchor='w')
ctk.CTkButton(frame_input, text="Buku Saya", command=search).pack(pady=5)

# Frame untuk menampilkan data peminjaman
frame_data = ctk.CTkFrame(app)
frame_data.pack(pady=10, fill='both', expand=True)

# Frame untuk input pengembalian buku (optional, can be removed if not needed)
frame_return = ctk.CTkFrame(app)
frame_return.pack(pady=10)

app.mainloop()
