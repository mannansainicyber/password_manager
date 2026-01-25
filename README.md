# Local Password Manager

A secure local password manager written in Python.

## Features
- Master password authentication
- PBKDF2 key derivation
- AES encryption (Fernet)
- Password generator
- Password strength & entropy checker
- Encrypted local vault

## Tech
- Python
- cryptography
- PBKDF2 + Fernet (AES)
- CLI-based interface

## Security Notes
- Vault is encrypted at rest
- Master password is never stored
- Salted key derivation is used

## Disclaimer
Educational project. Do not use for production secrets.
