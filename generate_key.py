import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('encryption_key.key', 'wb') as file:
    file.write(key)