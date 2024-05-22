import pandas as pd
from tkinter import messagebox

def login():
    dataUser    = pd.read_csv("database\\databaseUser.csv")
    df          = pd.DataFrame(dataUser)

    global user
    global password1
    user = email_entry.get()
    password1 = password1_entry.get()

    matching_creds = (len(df[(df.email == user) & (df.password1 == password1)]))

    if matching_creds:
        print("success")
        ds_pf()
    else:
        print("e-Mail belum terdaftar!")
        print("e-Mail/password salah"
        )