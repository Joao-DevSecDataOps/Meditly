from cryptography.fernet import Fernet
key = Fernet.generate_key()
print("Sua nova chave de criptografia é:")
print(key.decode())
print("\nCopie esta chave e cole-a no seu arquivo .env como DATA_ENCRYPTION_KEY")