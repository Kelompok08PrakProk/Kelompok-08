import sys
import os

# Module path (assuming modules are in the same directory)
module_path = os.path.join(os.path.dirname(__file__), "modul")
sys.path.append(module_path)

# Import modules
from loginregist import register_user, login_user, menuDua

# Main menu function
def main():
    logged_in = False  # Initialize the flag for login status
    while not logged_in:  # Run the loop until logged_in becomes True
        print("=" * 20)
        print("        PETI        ")
        print("=" * 20)
        print("===     Menu     ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        print("=" * 20)
        menu = int(input("Menu pilihan (1/2/3): "))

        if menu == 1:
            user_email = login_user()
            if user_email:
                logged_in = True
                menuDua(user_email)
        elif menu == 2:
            register_user()
            print("Terima kasih telah menggunakan program ini.")
            break
        elif menu == 3:
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()