from Cryptodome.Cipher import AES, ChaCha20
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad


KEY_SIZE_BYTES = 32
BLOCK_SIZE_BYTES = 16


def encrypt_text(password: str, text: str) -> dict[str, bytes]:
    key = pwd2key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    text = pad(bytes(text, 'utf-8'), BLOCK_SIZE_BYTES)
    return {'ciphertext': cipher.encrypt(text), 'iv': cipher.iv}


def decrypt_text(password: str, iv: bytes, ciphertext: bytes) -> str:
    key = pwd2key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    decrypted = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted, BLOCK_SIZE_BYTES).decode()
    return decrypted


def encrypt_file(password: str, filedata: bytes) -> dict[str, bytes]:
    key = pwd2key(password)
    nonce = get_random_bytes(24)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return {'ciphertext': cipher.encrypt(filedata), 'nonce': nonce}


def decrypt_file(password: str, nonce: bytes, ciphertext: bytes) -> bytes:
    key = pwd2key(password)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext)


def pwd2key(pwd: str):
    # salt is kept constant as salting is done by AES's 'iv' later.
    salt = "This will be constant"
    key = scrypt(pwd, salt, KEY_SIZE_BYTES, 2**14, 8, 1)
    return key
