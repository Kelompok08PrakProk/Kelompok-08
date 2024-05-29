def halaman_registration_successful():
    global window4
    window4 = ctk.CTk()
    window4.title("")
    window4.geometry("400x200")
    window4.resizable(False, False)

    frame = ctk.CTkFrame(window4, width=300, height=150, corner_radius=4, fg_color="White")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    l1 = ctk.CTkLabel(frame, text="Registrasi berhasil!", text_color="#1A1F23", font=('Trebuchet MS', 20))
    l1.place(relx=0.5, rely=0.3, anchor="center")

    l2 = ctk.CTkLabel(frame, text="Kembali ke halaman login dalam beberapa detik.", text_color="#1A1F23", font=('Trebuchet MS', 11))
    l2.place(relx=0.5, rely=0.5, anchor="center")

    def redirect_to_login():
        window4.destroy()
        halaman_login()

    window4.after(3000, redirect_to_login)

    window4.mainloop()