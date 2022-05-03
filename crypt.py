from cryptography.fernet import Fernet


def generate_key(file_location="secret.key"):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(file_location, "wb") as key_file:
        key_file.write(key)


def load_key(file_name="secret.key"):
    """
    Load the previously generated key
    """
    return open(file_name, "rb").read()


def encrypt_data(message, key):
    """
    Encrypts a message
    """
    encoded_message = str(message).encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt_data(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode("ascii")
