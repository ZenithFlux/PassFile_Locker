# 🔐️ PassFile Locker 

PassFile Locker is a secure password manager and a file encryption application for the people who like to store their passwords themselves instead of an online password manager. 

It has highly secure encryption for passwords and files. Your passwords are encrypted using the master password you provide and converted into unrecognisable bytes which cannot be read or converted back without knowing the master password.

![PassFile GUI](https://i.ibb.co/PCnrRW1/UI.png)

## ✨️ Features

- ⚡ No installation required.
- 🔑 AES-256 encryption for passwords.
- 🗝️ XChaCha20 encryption for files.
- 🤺 Uses [scrypt](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt) for key derivation, disabling brute force attacks.
- 🧂 All encryptions are fully salted, i.e. even when encrypting same data with the same password, different ciphertext is generated each time.
- 💼 Everything is saved in a portable **.lkr** file, so that you can store it anywhere (Even in Google Drive; google will have no idea about your passwords).
- 🎨 Both GUI and CLI modes are available.
- 🤩 So simple to use that there is no need for a manual.

> ❗❗**Note:** Only file contents are encrypted, not file names, therefore don't store any sensitive information in file names.

## 😇 How to use

### On Windows

1. Download [passfile-gui-2.0.1-win-x64.zip](https://github.com/ZenithFlux/PassFile_Locker/releases/download/v2.0.1/passfile-gui-2.0.1-win-x64.zip).  
    If you want the CLI version, download [passfile-cli-2.0.1-win-x64.zip](https://github.com/ZenithFlux/PassFile_Locker/releases/download/v2.0.1/passfile-cli-2.0.1-win-x64.zip). 

2. Extract the zip file. Run ***passfile.exe*** inside the **passfile** folder.

**Note:** After you have created a [.lkr file](#lkr-file), you can open it directly by selecting the above ***passfile.exe*** in *Open with* > *Choose another app...* option or when  Windows prompts you after double-clicking the file.

### On Linux

1. Download [passfile-gui-2.0.1-linux-x64.zip](https://github.com/ZenithFlux/PassFile_Locker/releases/download/v2.0.1/passfile-gui-2.0.1-linux-x64.zip).  
    If you want the CLI version, download [passfile-cli-2.0.1-linux-x64.zip](https://github.com/ZenithFlux/PassFile_Locker/releases/download/v2.0.1/passfile-cli-2.0.1-linux-x64.zip). 

2. Extract the zip file. Run the ***passfile*** executable inside the **passfile** folder.

**Note:** After you have created a [.lkr file](#lkr-file), you can open it directly by opening it with the above ***passfile*** executable. Your Linux distro may ask you to choose a program to open it with when you double-click the file.

### Using Python

*App was originally written in Python v3.12.1*

1. Clone the repo and move into it.
    ```sh
    git clone https://github.com/ZenithFlux/PassFile_Locker.git && cd PassFile_Locker
    ```
2. Install the requirments using pip.
    ```sh
    pip install -r requirements.txt
    ```
3. Run either *gui.py* or *cli.py* as per your wish.
    ```sh
    python gui.py
    ```
    OR
    ```sh
    python cli.py
    ```

#### Building executable

If you want to build a standalone PassFile executable for your platform, follow these additional steps:

4. Install pyinstaller and pillow using pip. Pillow because sometimes pyinstaller needs it to generate the app icon.
    ```sh
    pip install pyinstaller==6.4.0 pillow==10.2.0
    ```
5. Run the following commands:  
    **For GUI version:**
    ```sh
    pyinstaller -w --contents-directory . --add-binary=icon.png:. --icon=icon.png -n=passfile gui.py
    ```
    **For CLI version:**
    ```sh
    pyinstaller --contents-directory . --icon=icon.png -n=passfile cli.py
    ```

6. You will find the built application in ***dist*** folder.

## .lkr file

.lkr is the extension of the locker file created by the program. Double clicking .lkr file will prompt you for the password if opened with *gui.py*, *cli.py*, *passfile.exe*(Windows) or *passfile* executable(Linux).

Download the packaged zip files from [releases](https://github.com/ZenithFlux/PassFile_Locker/releases) section on github to get a pre-built executable for the program.

## Encryption Used

**AES-256 Encyption is used for passwords:** Extremely secure encryption method. Anything encrypted with AES has never been broken till date.

**XChaCha20 Encryption is used for files:** A less resource intensive encryption, hence it is used here to encrypt files. Also popular as highly secure stream cipher. 

## Notable Issues

Adding, deleting, renaming or extracting files with very large size takes some time to complete. During that time GUI will become unresponsive since there is no loading screen in the application yet. Users are advised to patiently wait for the application to complete its operations.

Similar issue can also occur when locker size is very large.

Due to the above reasons, size limit is set to 2GB for a single file, and 3GB for the whole locker.

## Credits

**icon.png:** [Password icons created by kawalanicon - Flaticon](https://www.flaticon.com/free-icons/password)
