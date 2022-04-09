# PassFile Locker

PassFile Locker is a password manager and a file storage (or file hiding) application. It has double layer encryption for passwords and single layer encryption for files. As first layer of encryption, the program converts all its data into binary form and then stores it. So, your data cannot be accessed through any of the commonly used programs like notepad etc. As the second layer, your passwords are encrypted based on the key you provided and converted into unrecognisable bytes which cannot be read or converted back without knowing the key, even by the developer of PassFile.

It is advised to keep your key length around 16 characters for best security (16 characters are ideal). Though key length has a little impact on security if your key is good enough.

All the instructions are embedded into the program.

## .lkr file

.lkr is the extension of the locker file created by the program. Double clicking the .lkr file has no use if program is not running from .exe file.

'.lkr' files can be opened directly when opened with passfile.exe. Download packaged app from the 'releases' section on github for the .exe file of the program.

## Encryption Used

AES-128 Encyption is used for passwords- Extremely secure encryption method. Any password encrypted with AES has never been broken till date.

ChaCha20 Encryption is used for files - A less resource intensive encryption, hence it is used here to encrypt files. Also popular as highly secure stream cipher. 

## Notable Issues

Adding, deleting, renaming or extracting files with very large size takes some time to complete. During that time GUI will become unresponsive since there is no loading screen in the application yet. Users are advised to just wait patiently for application to complete its operations.

Similar issue can also happen when locker size is very large.

Due to above reasons, size limit is set to 2GB for a single file, and 3GB for a whole locker.