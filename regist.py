import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import csv
import smtplib
import os
from customtkinter import *

class RegistrationForm(CTk):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PETI DEPENDABLE LIBRARY - Registration")

        self.username_label = ttk.Label(self, text="Username:")
        self.username_input = ttk.Entry(self)

        self.email_label = ttk.Label(self, text="Email:")
        self.email_input = ttk.Entry(self)

        self.password1_label = ttk.Label(self, text="Password:")
        self.password1_input = ttk.Entry(self, show="*")

        self.password2_label = ttk.Label(self, text="Confirm Password:")
        self.password2_input = ttk.Entry(self, show="*")

        self.fullname_label = ttk.Label(self, text="Full Name:")
        self.fullname_input = ttk.Entry(self)

        self.address_label = ttk.Label(self, text="Address:")
        self.address_input = ttk.Entry(self)

        self.phone_label = ttk.Label(self, text="Phone Number:")
        self.phone_input = ttk.Entry(self)

        self.register_button = ttk.Button(self, text="Register", command=self.register_user)

        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_input.grid(row=0, column=1, padx=5, pady=5)
        self.email_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_input.grid(row=1, column=1, padx=5, pady=5)
        self.password1_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password1_input.grid(row=2, column=1, padx=5, pady=5)
        self.password2_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.password2_input.grid(row=3, column=1, padx=5, pady=5)
        self.fullname_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.fullname_input.grid(row=4, column=1, padx=5, pady=5)
        self.address_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.address_input.grid(row=5, column=1, padx=5, pady=5)
        self.phone_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.phone_input.grid(row=6, column=1, padx=5, pady=5)
        self.register_button.grid(row=7, column=1, padx=5, pady=5)

    def register_user(self):
        username = self.username_input.get()
        email = self.email_input.get()
        password1 = self.password1_input.get()
        password2 = self.password2_input.get()
        namalengkap = self.fullname_input.get()
        alamat = self.address_input.get()
        nomorHP = self.phone_input.get()

        if password1 != password2:
            messagebox.showerror("Error", "Passwords do not match")
           