import re
import math

def calculate_entropy(password: str) -> float:
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[^\w]", password):
        charset_size += 32

    return len(password) * math.log2(charset_size) if charset_size else 0


def check_strength(password: str) -> dict:
    issues = []

    if len(password) < 12:
        issues.append("Password too short")

    sequential_chars = "abcdefghijklmnopqrstuvwxyz01234567890"
    if any(sequential_chars[i:i+4] in password.lower() for i in range(len(sequential_chars)-3)):
        issues.append("Avoid sequences like 'abc' or '123'")

    if not re.search(r"[a-z]", password):
        issues.append("Missing lowercase letter")
    if not re.search(r"[A-Z]", password):
        issues.append("Missing uppercase letter")
    if not re.search(r"[0-9]", password):
        issues.append("Missing digit")
    if not re.search(r"[^\w]", password):
        issues.append("Missing symbol")

    entropy = calculate_entropy(password)

    if entropy < 50:
        level = "WEAK"
    elif entropy < 70:
        level = "MEDIUM"
    else:
        level = "STRONG"

    score = min(int(entropy), 100)

    return {
        "score": score,
        "level": level,
        "entropy": round(entropy, 2),
        "issues": issues,
        "Protocol": "v1"
    }
