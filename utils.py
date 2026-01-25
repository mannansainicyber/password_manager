import os, json, base64, hashlib
META_FILE = "meta.json"

def set_master_password(master_password: str):
    if os.path.exists(META_FILE):
        raise Exception("Master password already set")

    salt = os.urandom(16)

    verify_hash = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode(),
        salt,
        100_000
    )

    with open(META_FILE, "w") as f:
        json.dump({
            "salt": base64.b64encode(salt).decode(),
            "verify": base64.b64encode(verify_hash).decode()
        }, f)

    print("Master password set successfully")

def verify_master_password(master_password: str) -> bool:
    if not os.path.exists(META_FILE):
        return False

    with open(META_FILE, "r") as f:
        meta = json.load(f)

    salt = base64.b64decode(meta["salt"])
    stored_hash = base64.b64decode(meta["verify"])

    check_hash = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode(),
        salt,
        100_000
    )

    return check_hash == stored_hash

