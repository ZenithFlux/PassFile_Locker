import json
import pickle

from .encrypter import encrypt, decrypt


class Locker:

    CHECK_PHRASE_PLAINTEXT = 'correct_password'

    def __init__(self, password: str):
        self.check_phrase: dict[str, bytes] = {}
        self.passwords: dict[str, bytes] = { 'data': {} }
        self.files: dict[str, dict[str, bytes]] = {}

        self.check_phrase['ciphertext'], self.check_phrase['iv'] = encrypt(password, self.CHECK_PHRASE_PLAINTEXT)
        self.pwd = password


    def unlock(self, password: str) -> bool:
        unlocked = decrypt(password, self.check_phrase['iv'],
                           self.check_phrase['ciphertext']) == self.CHECK_PHRASE_PLAINTEXT
        if unlocked:
            self.pwd = password
            pwd_json = decrypt(password, self.passwords['iv'], self.passwords['ciphertext'])
            self.passwords['data'] = json.loads(pwd_json)

        return unlocked


    def add_file(self, filename: str, filedata: bytes):
        if not hasattr(self, "pwd"):
            raise LockerError("Locker not unlocked")

        self.files[filename] = {}
        self.files[filename]['ciphertext'], self.files[filename]['nonce'] = encrypt(self.pwd, filebytes = filedata)


    def change_password(self, new_pwd: str):
        if not hasattr(self, "pwd"):
            raise LockerError("Locker not unlocked")

        plaintext = decrypt(self.pwd, self.passwords['iv'], self.passwords['ciphertext'])
        self.passwords['ciphertext'], self.passwords['iv'] = encrypt(new_pwd, plaintext)

        for file in self.files.values():
            plaintext = decrypt(self.pwd, file['nonce'], filebytes = file['ciphertext'])
            file['ciphertext'], file['nonce'] = encrypt(new_pwd, filebytes = plaintext)

        self.check_phrase['ciphertext'], self.check_phrase['iv'] = encrypt(new_pwd, self.CHECK_PHRASE_PLAINTEXT)
        self.pwd = new_pwd


    def save(self, path: str):
        if not hasattr(self, "pwd"):
            raise LockerError("Locker not unlocked")

        pwd = self.pwd
        del self.pwd
        pwd_dict = self.passwords['data']
        del self.passwords['data']

        pwd_json = json.dumps(pwd_dict)
        self.passwords['ciphertext'], self.passwords['iv'] = encrypt(pwd, pwd_json)

        with open(path, 'wb') as f:
            pickle.dump(self, f)

        self.passwords['data'] = pwd_dict
        self.pwd = pwd



class LockerError(Exception):
    pass
