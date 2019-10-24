from cryptography.fernet import Fernet

print key
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
print cipher_text

print plain_text
