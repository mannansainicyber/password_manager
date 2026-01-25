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
            print("\n3. View service password")
            print("4. Generate password")
            print("5. Check password strength")
            print("6. List saved services")
            print("7. Add service manually")
            print("8. Delete service")
            print("9. Search services")
            print("10. Logout")
            print("11. Exit")

            choice = input("Select: ")

            if choice == "3":
                service = input("Service name: ")
                pwd = vault.get(service)
                if pwd:
                    print(f"Password for {service}: {pwd}")
                else:
                    print("Service not found")

            elif choice == "4":
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

            elif choice == "5":
                pwd = input("Enter password: ")
                print(check_strength(pwd))

            elif choice == "6":
                if not vault:
                    print("No services saved")
                for service in vault:
                    print("-", service)

            elif choice == "7":
                service = input("Service name: ")
                pwd = input("Password: ")
                if service in vault:
                    print("Service already exists")
                    print("Use 'Delete' option to remove it first")
                else:
                    vault[service] = pwd
                save_encrypted_vault(vault, key)
                print("Service added 🔐")

            elif choice == "8":
                service = input("Service to delete: ")
                if service in vault:
                    del vault[service]
                    save_encrypted_vault(vault, key)
                    print("Service deleted 🗑️")
                else:
                    print("Service not found")

            elif choice == "9":
                term = input("Search term: ").lower()
                matches = [s for s in vault if term in s.lower()]

                if matches:
                    print("Matches:")
                    for s in matches:
                        print("-", s)
                else:
                    print("No matching services")

            elif choice == "10":
                print("Logged out 🔒")
                break

            elif choice == "11":
                print("👋 Bye")
                exit()

            else:
                print("Invalid option")


if __name__ == "__main__":
    main()
