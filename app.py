import subprocess
import sys
import os
import json
import base64
from utils import set_master_password, verify_master_password
from generator import generate_password
from storage import derive_key, load_encrypted_vault, backup_vault
from session import Session
from ui import (
    display_menu,
    handle_view_password,
    handle_generate_password,
    handle_check_strength,
    handle_list_services,
    handle_add_service,
    handle_delete_service,
    handle_search_services,
    handle_backup,
    handle_logout,
    handle_exit,
    MENU_VIEW,
    MENU_GENERATE,
    MENU_CHECK_STRENGTH,
    MENU_LIST,
    MENU_ADD,
    MENU_DELETE,
    MENU_SEARCH,
    MENU_BACKUP,
    MENU_LOGOUT,
    MENU_EXIT,
)

META_FILE = "meta.json"


def install_dependencies():
    required_packages = ["cryptography"]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing dependency: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def auth():
    if not os.path.exists(META_FILE):
        master = input("Set a master password: ")
        set_master_password(master)
        return master

    tries = 0
    while tries < 3:
        master = input("Enter master password: ")
        if verify_master_password(master):
            print("Vault unlocked 🔓")
            return master
        tries += 1
        print("Wrong password")

    print("Too many tries!")
    exit()


def run_session(master, session):
    with open(META_FILE) as f:
        salt = base64.b64decode(json.load(f)["salt"])
    
    key = derive_key(master, salt)
    vault = load_encrypted_vault(key)
    session.start()
    
    commands = {
        MENU_VIEW: (handle_view_password, [vault]),
        MENU_GENERATE: (handle_generate_password, [vault, key, generate_password]),
        MENU_CHECK_STRENGTH: (handle_check_strength, []),
        MENU_LIST: (handle_list_services, [vault]),
        MENU_ADD: (handle_add_service, [vault, key]),
        MENU_DELETE: (handle_delete_service, [vault, key]),
        MENU_SEARCH: (handle_search_services, [vault]),
        MENU_BACKUP: (handle_backup, [backup_vault]),
        MENU_LOGOUT: (handle_logout, [session]),
        MENU_EXIT: (handle_exit, []),
    }
    
    while True:
        if not session.is_active():
            print("Session expired 🔒")
            break
        
        display_menu()
        choice = input("Select: ").strip()
        session.touch()
        
        if choice in commands:
            handler, args = commands[choice]
            result = handler(*args)
            if result == "logout":
                break
        else:
            print("Invalid option")


def main():
    print("🔐 Password Manager")
    session = Session()
    
    while True:
        master = auth()
        run_session(master, session)


if __name__ == "__main__":
    install_dependencies()
    main()