import os
import json
import base64
from utils import (
    set_master_password,
    verify_master_password,
)
from generator import generate_password
from strength import check_strength
from storage import (
    derive_key,
    load_encrypted_vault,
    save_encrypted_vault
)
META_FILE = "meta.json"


def auth():
    tries = 0

    if not os.path.exists(META_FILE):
        print("No master password found.")
        master = input("Set a master password: ")
        set_master_password(master)
        return master

    while tries < 3:
        master = input("Enter master password: ")
        if verify_master_password(master):
            print("Vault unlocked 🔓")
            return master
        else:
            tries += 1
            print("Wrong password")

    print("Too many tries!")
    exit()


def main():
    print("🔐 Password Manager")

    while True:
        # ---- AUTH ----
        master = auth()

        with open(META_FILE) as f:
            salt = base64.b64decode(json.load(f)["salt"])

        key = derive_key(master, salt)
        vault = load_encrypted_vault(key)

        # ---- MAIN MENU ----
        while True:
            print("\n1. Generate password")
            print("2. Check password strength")
            print("3. List saved services")
            print("4. Logout")
            print("5. Exit")

            choice = input("Select: ")

            if choice == "1":
                length = int(input("Password length: "))
                pwd = generate_password(length)

                result = check_strength(pwd)
                print("Generated:", pwd)
                print("Strength:", result["level"], "| Entropy:", result["entropy"])

                save = input("Save password? (y/n): ")
                if save.lower() == "y":
                    service = input("Service name: ")
                    vault[service] = pwd
                    save_encrypted_vault(vault, key)
                    print("Saved securely 🔐")

            elif choice == "2":
                pwd = input("Enter password: ")
                print(check_strength(pwd))

            elif choice == "3":
                for service in vault:
                    print("-", service)

            elif choice == "4":
                print("Logged out 🔒")
                break

            elif choice == "5":
                print("👋 Bye")
                exit()

            else:
                print("Invalid option")


if __name__ == "__main__":
    main()
