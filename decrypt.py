from cryptography.fernet import Fernet
from core.settings import settings
import json

cipher_suite = Fernet(settings.ENCRYPT_KEY)

with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
decrypted_data = cipher_suite.decrypt(encrypted_data)
token_dict = json.loads(decrypted_data.decode())
print(token_dict)