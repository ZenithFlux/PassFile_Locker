import json
import pickle

from .encrypter import encrypt_text, decrypt_text, encrypt_file, decrypt_file


class Locker:

    CHECK_PHRASE_PLAINTEXT = 'correct_password'

    def __init__(self, password: str):
        self.check_phrase: dict[str, bytes] = {}
        self.passwords: dict[str, bytes] = {}
        self.files: dict[str, dict[str, bytes]] = {}
        self.pwd_dict: dict[str, str] = {}
        self.pwd = password

        self.check_phrase = encrypt_text(password, self.CHECK_PHRASE_PLAINTEXT)


    def unlock(self, password: str) -> bool:
        try:
            unlocked = decrypt_text(password, **self.check_phrase) == self.CHECK_PHRASE_PLAINTEXT
        except ValueError:
            return False

        if unlocked:
            self.pwd = password
            pwd_json = decrypt_text(password, **self.passwords)
            self.pwd_dict = json.loads(pwd_json)

        return unlocked


    def change_password(self, new_pwd: str):
        if not hasattr(self, "pwd"):
            raise LockerError("Locker not unlocked")

        plaintext = decrypt_text(self.pwd, **self.passwords)
        self.passwords = encrypt_text(new_pwd, plaintext)

        for file in self.files:
            plaintext = decrypt_file(self.pwd, **self.files[file])
            self.files[file] = encrypt_file(new_pwd, plaintext)

        self.check_phrase = encrypt_text(new_pwd, self.CHECK_PHRASE_PLAINTEXT)
        self.pwd = new_pwd


    def save(self, path: str):
        if not hasattr(self, "pwd"):
            raise LockerError("Locker not unlocked")

        pwd = self.pwd
        del self.pwd
        pwd_dict = self.pwd_dict
        del self.pwd_dict

        pwd_json = json.dumps(pwd_dict)
        self.passwords = encrypt_text(pwd, pwd_json)

        with open(path, 'wb') as f:
            pickle.dump(self, f)

        self.pwd_dict = pwd_dict
        self.pwd = pwd


    def add_file(self, name: str, filedata: bytes):
        self.files[name] = encrypt_file(self.pwd, filedata)


    def remove_file(self, name: str):
        del self.files[name]


    def rename_file(self, name: str, new_name: str):
        self.files[new_name] = self.files[name]
        del self.files[name]


    def get_file(self, name: str) -> bytes:
        return decrypt_file(self.pwd, **self.files[name])



class LockerError(Exception):
    pass
