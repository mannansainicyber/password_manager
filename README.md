# Local Password Manager

A secure, lightweight password management system written in Python with encrypted local storage and CLI interface.

## Features

### Core Functionality
- **Master Password Authentication** - Single password protects all credentials
- **Password Storage & Retrieval** - Save and access passwords by service name
- **Password Generator** - Create strong, random passwords with customizable length
- **Password Strength Analyzer** - Check entropy, strength levels, and security recommendations
- **Vault Management** - Add, view, delete, and search stored passwords
- **Session Management** - Automatic 15-minute timeout for security

### Security
- **AES Encryption (Fernet)** - Industry-standard symmetric encryption
- **PBKDF2 Key Derivation** - Secure master password processing with 100,000 iterations
- **Salted Hashing** - Unique salt for each installation
- **Encrypted Vault** - All passwords encrypted at rest in `vault.enc`
- **Automatic Backups** - Timestamped backup system for disaster recovery

## Quick Start

### Installation
Dependencies install automatically on first run:
```bash
python app.py
```

Or install manually:
```bash
pip install cryptography
```

### First Time Setup
1. Run `python app.py`
2. Set your master password (store it securely!)
3. Start managing passwords

## Menu Options

| Option | Description |
|--------|-------------|
| 1 | View service password |
| 2 | Generate password |
| 3 | Check password strength |
| 4 | List saved services |
| 5 | Add service manually |
| 6 | Delete service |
| 7 | Search services |
| 8 | Backup vault |
| 9 | Logout |
| 10 | Exit |

## Project Structure

```
.
├── app.py              # Main application entry point
├── ui.py               # Menu handlers and UI logic
├── generator.py        # Password generation
├── strength.py         # Password strength analysis
├── storage.py          # Encryption/decryption & backup
├── session.py          # Session management & timeout
├── utils.py            # Master password hashing utilities
├── meta.json           # Master password salt (auto-generated)
├── vault.enc           # Encrypted password vault (auto-generated)
└── README.md           # This file
```

## Security Features

- **Auto-install Dependencies** - Missing packages installed automatically
- **Encrypted Vault** - Passwords stored in encrypted `vault.enc` file
- **Master Password** - Protected via PBKDF2 + SHA256 hashing
- **Session Timeout** - Auto-logout after 15 minutes of inactivity
- **Backup & Recovery** - Create timestamped backups of your vault
- **Salted Keys** - Each installation has unique salt for additional security

## Tech Stack

- **Python 3.7+** - Core language
- **cryptography** - AES encryption & key derivation
- **PBKDF2** - Password key derivation function
- **Fernet** - Symmetric encryption
- **CLI** - Command-line interface

## Configuration

### Session Timeout
Default: 15 minutes. Modify in `session.py`:
```python
SESSION_TIMEOUT = 5 * 60  # Change to desired seconds
```

### Backup Location
Backups stored in: `backups/backup_YYYYMMDD_HHMMSS/`

## Master Password Tips

- Use 20+ characters for strong security
- Mix uppercase, lowercase, digits, and symbols
- Store securely (password manager, secure note, etc.)
- **NEVER** forget it - recovery is impossible

## Important Notes

- **Educational Project** - Do not use for production secrets
- **Local Only** - No cloud sync or multi-device support
- **Single User** - Designed for local use only
- **No Recovery** - Lost master password = lost access

## Documentation

SOON
## License

Educational project - use at your own risk

## Contributing

Feel free to fork, improve, and contribute back!
