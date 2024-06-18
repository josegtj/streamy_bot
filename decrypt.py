from cryptography.fernet import Fernet
import json
import os

key = os.getenv("ENCRYPT_KEY")
cipher_suite = Fernet(key)

with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
decrypted_data = cipher_suite.decrypt(encrypted_data)
token_dict = json.loads(decrypted_data.decode())
print(token_dict)