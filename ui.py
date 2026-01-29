from strength import check_strength
from storage import save_encrypted_vault

MENU_VIEW = "1"
MENU_GENERATE = "2"
MENU_CHECK_STRENGTH = "3"
MENU_LIST = "4"
MENU_ADD = "5"
MENU_DELETE = "6"
MENU_SEARCH = "7"
MENU_BACKUP = "8"
MENU_LOGOUT = "9"
MENU_EXIT = "10"


def display_menu():
    print("\n=== Password Manager Menu ===")
    print(f"{MENU_VIEW}. View service password")
    print(f"{MENU_GENERATE}. Generate password")
    print(f"{MENU_CHECK_STRENGTH}. Check password strength")
    print(f"{MENU_LIST}. List saved services")
    print(f"{MENU_ADD}. Add service manually")
    print(f"{MENU_DELETE}. Delete service")
    print(f"{MENU_SEARCH}. Search services")
    print(f"{MENU_BACKUP}. Backup vault")
    print(f"{MENU_LOGOUT}. Logout")
    print(f"{MENU_EXIT}. Exit")


def get_password_length():
    while True:
        try:
            length = int(input("Password length: "))
            if length < 1:
                print("Length must be positive")
                continue
            return length
        except ValueError:
            print("Please enter a valid number")


def handle_view_password(vault):
    service = input("Service name: ")
    password = vault.get(service)
    if password:
        print(f"Password: {password}")
    else:
        print("Service not found")


def handle_generate_password(vault, key, generate_password_func):
    length = get_password_length()
    pwd = generate_password_func(length)
    result = check_strength(pwd)
    
    print(f"Generated: {pwd}")
    print(f"Strength: {result['level']} | Entropy: {result['entropy']}")
    
    if input("Save password? (y/n): ").lower() == "y":
        service = input("Service name: ")
        vault[service] = pwd
        save_encrypted_vault(vault, key)
        print("Saved securely 🔐")


def handle_check_strength():
    pwd = input("Enter password: ")
    result = check_strength(pwd)
    print(f"Strength: {result['level']} | Entropy: {result['entropy']} | Score: {result['score']}/100")
    if result['issues']:
        print("Issues:")
        for issue in result['issues']:
            print(f"  - {issue}")


def handle_list_services(vault):
    if not vault:
        print("No services saved")
        return
    
    print("\nSaved services:")
    for service in vault:
        print(f"  - {service}")


def handle_add_service(vault, key):
    service = input("Service name: ")
    
    if service in vault:
        print("Service already exists")
        return
    
    pwd = input("Password: ")
    vault[service] = pwd
    save_encrypted_vault(vault, key)
    print("Service added 🔐")


def handle_delete_service(vault, key):
    service = input("Service to delete: ")
    
    if service in vault:
        del vault[service]
        save_encrypted_vault(vault, key)
        print("Service deleted 🗑️")
    else:
        print("Service not found")


def handle_search_services(vault):
    term = input("Search term: ").lower()
    matches = [s for s in vault if term in s.lower()]
    
    if matches:
        print("\nMatching services:")
        for service in matches:
            print(f"  - {service}")
    else:
        print("No matching services")


def handle_backup(backup_vault_func):
    backup_vault_func()
    print("Backup created ✓")


def handle_logout(session):
    print("Logged out 🔒")
    session.end()
    return "logout"


def handle_exit():
    print("👋 Bye")
    exit()
