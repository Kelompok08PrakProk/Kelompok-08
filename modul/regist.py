import pandas as pd

def regist():
    dataUser = pd.read_csv("database\\databaseUser.csv")
    df = pd.DataFrame(dataUser)

    global user
    global password1
    global password2
    global username
    global namalengkap
    global alamat
    global nomorHP

    user        = email_entry2.get()
    password1   = password1_entry.get()
    password2   = password2_entry.get()
    username    = username_entry.get()
    namalengkap = namalengkap_entry.get()
    alamat      = alamat_entry.get()
    nomorHP     = nomorHP_entry.get()

    matching_creds = (len(df[(df.email == user) ]) < 1)

    if matching_creds and user != "":
        print("success")
        userBaru    = {"email"      : [user],
                       "password1"  : [password1],
                       "password2"  : [password2],
                       "username"   : [username],
                       "alamat"     : [alamat],
                       "nomorHP"    : [nomorHP]}
        registuser  = pd.DataFrame(userBaru)
        registuser.to_csv("database\\databaseUser.csv", mode="a", index=False, header=False)
        messagebox.showinfo("Register Page", "Akun Anda berhasil dibuat")
        s_rs.destroy()
    else:
        s_rs.destroy()
        messagebox.showinfo("Register Page", "Password harus sesuai, mohon periksa kembali!")
        registerscreen()