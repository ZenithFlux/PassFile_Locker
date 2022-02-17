# PassFile Locker

PassFile Locker is a password manager and a file storage (or file hiding) application. It has double layer encryption for passwords and single layer encryption for files. As first layer of encryption, the program converts all its data into binary form and then stores it. So, your data cannot be accessed through any of the commonly used programs like notepad etc. As the second layer, your passwords are encrypted based on the key you provided and converted into unrecognisable bytes which cannot be read or converted back without knowing the key, even by the developer of PassFile.

It is advised to keep your key as long as possible (upto 32 characters) as this program works on the principle 'the longer the key, the more secure the encryption'.

All the instructions are embedded into the program.

## .lkr file

.lkr is the extension of the locker file created by the program. Double clicking the .lkr file has no use if program is not running from .exe file.
Go to my Executables repository for the .exe file of the program. '.lkr' files can be opened directly when opened with passfile.exe.

## Encryption Used

AES Encyption is used for passwords- Extremely secure encryption method. Any password encrypted with AES has never been broken till date.

ChaCha20 Encryption is used for files - A less resource intensive encryption, hence it is used here to encrypt files. Also popular as highly secure stream cipher. 