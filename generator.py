import string
import secrets

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    if length < 4:
        print("Warning: length too short, using 12")
        length = 12

    characters = string.ascii_lowercase
    mandatory = []

    if use_upper:
        characters += string.ascii_uppercase
        mandatory.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        characters += string.digits
        mandatory.append(secrets.choice(string.digits))
    if use_symbols:
        characters += string.punctuation
        mandatory.append(secrets.choice(string.punctuation))

    remaining_length = length - len(mandatory)
    password_chars = [secrets.choice(characters) for _ in range(remaining_length)]

    password_chars += mandatory
    secrets.SystemRandom().shuffle(password_chars)

    password = ''.join(password_chars)
    return password
