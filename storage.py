import json
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

VAULT_FILE = "vault.json"
META_FILE = "meta.json"


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def init_vault(master_password: str):
    if os.path.exists(META_FILE):
        return

    salt = os.urandom(16)
    key = derive_key(master_password, salt)

    with open(META_FILE, "w") as f:
        json.dump({
            "salt": base64.b64encode(salt).decode()
        }, f)

    with open(VAULT_FILE, "w") as f:
        json.dump({}, f)


def save_password(master_password: str, service: str, password: str):
    with open(META_FILE, "r") as f:
        salt = base64.b64decode(json.load(f)["salt"])

    key = derive_key(master_password, salt)
    cipher = Fernet(key)

    encrypted = cipher.encrypt(password.encode()).decode()

    data = {}
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)

    data[service] = encrypted

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_password(master_password: str, service: str):
    with open(META_FILE, "r") as f:
        salt = base64.b64decode(json.load(f)["salt"])

    key = derive_key(master_password, salt)
    cipher = Fernet(key)

    with open(VAULT_FILE, "r") as f:
        data = json.load(f)

    encrypted = data.get(service)
    if not encrypted:
        return None

    return cipher.decrypt(encrypted.encode()).decode()


def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    return f.encrypt(json_data)

def decrypt_data(token: bytes, key: bytes) -> dict:
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return json.loads(decrypted.decode())

def save_encrypted_vault(data: dict, key: bytes):
    encrypted = encrypt_data(data, key)
    with open("vault.enc", "wb") as f:
        f.write(encrypted)
        
def load_encrypted_vault(key: bytes):
    if not os.path.exists("vault.enc"):
        return {}

    with open("vault.enc", "rb") as f:
        encrypted = f.read()

    return decrypt_data(encrypted, key)
