from Cryptodome.Cipher import AES, ChaCha20
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad


KEY_SIZE_BYTES = 32
BLOCK_SIZE_BYTES = 16

class LockerError(Exception):
    pass


def encrypt(password: str, text: str | None = None, filebytes: bytes | None = None):
    if text is not None:
        key = pwd2key(password)
        cipher = AES.new(key, AES.MODE_CBC)

        text = pad(bytes(text, 'utf-8'), BLOCK_SIZE_BYTES)
        encrypted = cipher.encrypt(text)
        iv_or_nonce = cipher.iv

    elif filebytes is not None:
        key = pwd2key(password)
        nonce = get_random_bytes(12)

        cipher = ChaCha20.new(key, nonce)
        encrypted = cipher.encrypt(filebytes)
        iv_or_nonce = nonce

    else:
        raise ValueError("Either 'text' or 'filebytes' must be provided")

    return encrypted, iv_or_nonce


def decrypt(password: str, iv_or_nonce: bytes, text: bytes | None = None, filebytes: bytes | None = None):
    if text is not None:
        key = pwd2key(password)
        cipher = AES.new(key, AES.MODE_CBC, iv = iv_or_nonce)

        decrypted = cipher.decrypt(text)
        decrypted = unpad(decrypted, BLOCK_SIZE_BYTES).decode()

    elif filebytes is not None:
        key = pwd2key(password)
        cipher = ChaCha20.new(key, iv_or_nonce)

        decrypted = cipher.decrypt(filebytes)

    else:
        raise ValueError("Either 'text' or 'filebytes' must be provided")

    return decrypted


def pwd2key(pwd: str):
    # salt is kept constant as salting is done by AES's 'iv' later.
    salt = "This will be constant"
    key = scrypt(pwd, salt, KEY_SIZE_BYTES, 2**14, 8, 1)
    return key
