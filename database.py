def save_data(encrypted_data):
    with open("data.crypt", "w") as file:
        data = encrypted_data.decode()
        file.write(data)
        file.close()


def load_data():
    try:
        with open("data.crypt", "r") as file:
            # Reading from a file
            token_dec = file.read()
            file.close()
            return token_dec
    except FileNotFoundError:
        print("Cant find file specified. create it now?")
        with open("data.crypt", "w") as f:
            f.close()
            return ""


def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()
