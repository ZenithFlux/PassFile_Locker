'''
This is an early development version of PassFile Locker. This application operates only on command line interface currently, 
gui will be added just before finalizing the project.
'''

from functions import encrypt, decrypt
from functions.encrypter import LockerError
import sys
from Crypto.Random import get_random_bytes
import os
import pickle
from pwinput import pwinput


class LockerData:
    def __init__(self, key, iv):
        self.key = key
        self.passwords = {}
        self.files = {}
        self.iv = iv
        

def newLocker(file, key):
    print('Creating new Locker...')
    iv = get_random_bytes(16)
    data = LockerData(encrypt(key, key, iv), iv)
    
    save(file, data)
    
    clrscr()
    openLocker(file, key)
    return
 
 
    
def openLocker(file, key):
    
    print("Opening the Locker...")   
    with open(file, 'rb') as f:
        data = pickle.load(f)
    clrscr()

    if decrypt(data.key, key, data.iv) == key:
        passmode(data, key)
        
    else:
        raise LockerError('Invalid key')

    
def passmode(data, key):
    global file
    
    while True:
        passwords = data.passwords
        print("---- {0} ----\n--Password Section--".format(file.split('\\')[-1]))
        
        if not passwords:
            print('\nNo password added yet...')
        
        else:
            print("\nSites for which passwords have been found -")
            n=0    
            for site in passwords.keys():
                n += 1
                print(f'{n}. {site}')
            del n
            print()
        
        if passwords:
            print('Enter the number of a site to view/change/delete your password entered for the site.')
        print("Type 'add' to add a new password.\nType 'f' to go into Files Section.\nType 'exit' to close the locker.")
        choice = input().lower()

        if choice == 'f':
            clrscr()
            file_closed = filemode(data, key)
            if file_closed == True:
                return
            else:
                continue
        
        if choice == 'exit':
            return
        
        elif choice == 'add':
            site = input("Enter a new site name to store password for: ")
            if site in passwords:
                print('Password for this site already exists!\n')
                continue
            elif site.lower() == 'exit':
                clrscr()
                continue
            
            newPass = pwinput('Enter the password to store: ')
            clrscr()
            
            if newPass.lower() == 'exit':
                continue
            
            if '~' in newPass:
                print("Keys and passwords cannot contain '~'!\n")
                continue
            
            data.passwords[site] = encrypt(newPass, key, data.iv)
            save(file, data)
            print('New password added successfully...\n')
            continue
         
        elif not passwords:
            clrscr()
            print('Invalid input!\n')
            continue
        
        elif choice.isnumeric() and int(choice) <= len(passwords.keys()):
            site = list(passwords.keys())[int(choice) - 1]
            password = decrypt(passwords[site], key, data.iv)
            print(f"\nPassword for '{site}' is:\n{password}")
            print("Type 'change' to change this password.")
            print("Type 'delete' to delete this password. Password can't be retrieved once deleted.")
            print("Enter 'b' to go back to site selection menu.")
            choice = input().lower()
            clrscr()
            
            if choice == 'b' or choice == 'exit':
                clrscr()
                continue
            
            elif choice == 'change':
                newPass = pwinput("Enter new password: ")
                clrscr()
                
                if newPass.lower() == 'exit':
                    continue
                
                if '~' in newPass:
                    print("Keys and passwords cannot contain '~'!\n")
                    continue
                
                data.passwords[site] = encrypt(newPass, key, data.iv)
                save(file, data)
                print('Password updated successfully...\n')
                continue
            
            elif choice == 'delete':
                del data.passwords[site]
                save(file, data)
                print("Password deleted successfully...\n")
                continue
            
            else:
                print('Invalid input!\n')
                continue
            
        else:
            clrscr()
            print('Invalid input!\n')
            continue
        
def filemode(data, key):
    global file
    print("This locker is designed to encrypt important documents. Since encryption is very resource intensive,")
    print("it is not advised to put huge files in the locker. Locker will take more time to encrypt bigger files.\n")
    print("If you want to store large number of files, you can zip those files and store it here.\n")
    
    if '\\' in file:
        defaultpath = '\\'.join(file.split("\\")[:-1]) + '\\'     # removing locker's name from the end of the path
    else:
        defaultpath = ''
        
    while True:
        print("---- {0} ----\n--Files Section --".format(file.split('\\')[-1]))
        
        if not data.files:
            print('\nNo Files found in the locker...')
        
        else:
            print("\nFollowing files have been found in the locker -")
            n=0    
            for filename in data.files.keys():
                n += 1
                print(f'{n}. {filename}')
            del n
            print()
        
        if data.files:
            print('Enter the number of a file to extract/rename/delete that file.')
            
        print("Type 'add' to add a new file.\nType 'p' to go into Password Section.\nType 'exit' to close the locker.")
        choice = input().lower()
        
        if choice == 'p':
            clrscr()
            return False
            
        elif choice == 'add':
            filename = input("Enter path of the file to add: ")
            if filename.lower() == 'exit':
                clrscr()
                continue
            
            if '\\' not in filename:
                filename = defaultpath + filename      
                
            try:
                if (os.path.getsize(file) + os.path.getsize(filename)) > 3*1024*1024*1024:
                    clrscr()
                    print("Adding this file will exceed the locker limit (3 GB)!!\n")
                    continue
                
                with open(filename, 'rb') as f:
                    if os.path.getsize(filename) > 2*1024*1024*1024:   # 2 GB = 2*1024*1024*1024 bytes
                        clrscr()
                        print('File too large to add. Size limit per file is set to 2 GB for performance purposes!!\n')
                        continue
                    
                    print("Processing the file...")    
                    data.files[filename.split('\\')[-1]] = encrypt(None, key, 0, filebytes = f.read())
                    
            except FileNotFoundError:
                clrscr()
                print(filename)
                print("File not found!\n")
                continue
            
            save(file, data)
            clrscr()
            print("File added successfully...\nFrom " + filename +'\n')
            continue
        
        elif choice == 'exit':
            return True
            
        elif not data.files:
            clrscr()
            print('Invalid input!\n')
            continue
            
        elif choice.isnumeric() and int(choice) <= len(data.files):
            filename = list(data.files.keys())[int(choice) - 1]
            print(f"--- {filename} ---\n")
            print("Type 'extract' to extract the file.\nType 'rename' to rename it.")
            print("Type 'delete' to remove the file from the locker.\nEnter 'b' to go back to the files list.")
            choice = input().lower()
            
            if choice == "b" or choice == "exit":
                clrscr()
                continue
            
            elif choice == "rename":
                newName = input("Enter new name for the file: ")
                if newName.lower() == 'exit':
                    clrscr()
                    continue
                
                print("Renaming the file...")
                data.files[newName] = data.files[filename]
                del data.files[filename]
                save(file, data)
                
                clrscr()
                print("File renamed successfully...\n")
                continue
            
            elif choice == "delete":
                print("Deleting the file...")
                del data.files[filename]
                save(file, data)
                clrscr()
                print("File deleted successfully...\n")
                continue
            
            elif choice == "extract":
                extractpath = input("\nEnter the location to extract the file.\nPress 'Enter' to extract at the locker location.\n")
                if extractpath.lower() == 'exit':
                    clrscr()
                    continue
                
                if extractpath != '':
                    extractpath = extractpath + '\\' + filename
                    
                else:
                    extractpath = defaultpath + filename
                try:
                    print("Extracting the file...")
                    with open(extractpath, 'wb') as f:
                        f.write(decrypt(None, key, 0, filebytes = data.files[filename]))
                
                except FileNotFoundError:
                    clrscr()
                    print(extractpath)
                    print('No such folder exists!\n')
                    continue
                
                except PermissionError:
                    clrscr()
                    print(extractpath)
                    print("No Permission to write this folder!!\n")
                    continue
                
                clrscr()
                print("File successfully extracted...\nTo " + extractpath +'\n')
                continue
            
            else:
                clrscr()
                print('Invalid Input!\n')
                continue
            
        else:
            clrscr()
            print('Invalid input!\n')
            continue
            

# Micro Functions----------------------------------------------------------------------------------------------

def save(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)
        
def clrscr():
    os.system('cls')       


# Main Program--------------------------------------------------------------------------------------------------

def main():
    
    global file
    if len(sys.argv) >= 2:
        file = sys.argv[1]
        key = pwinput("Enter key: ")
        clrscr()
        try:
            print("You can type 'exit' anytime while using this application to go back.\n")
            openLocker(file, key)
        except LockerError:
            print('Invaild key!!')
            e = input('Press Enter to exit the window...\n')
            sys.exit()
        except:
            print("Something went wrong...")
            e = input('Press Enter to exit the window...\n')
            sys.exit()
        sys.exit()
            
    
    print("You can type 'exit' anytime while using this application to go back.\n")
    while True:
        print('What should we do?\n1. Open a locker\n2. Create new locker\n3. Exit')
        choice = input('Enter your choice no.: ')
        
        if choice == '1':
            file = input("Enter the filename with path: ")
            
            if file.lower() == 'exit':
                clrscr()
                continue
            
            if not file.endswith('.lkr'):
                file = file + '.lkr'
                
            if not os.path.exists(file):
                clrscr()
                print(f'Such file does not exist!\n')
                continue
                
            key = pwinput("Enter key: ")
            clrscr()
            if key.lower() == 'exit':
                clrscr()
                continue
            
            try:
                openLocker(file, key)
                clrscr()
            except LockerError:
                print('Invaild key!!\n')
                continue
            
        elif choice == '2':
            file = input("Enter name and path for the new Locker file: ")
            if file.lower() == 'exit':
                clrscr()
                continue
            if not file.endswith('.lkr'):
                file = file + '.lkr'
                
            key = pwinput("Enter key for the locker (Warning: Once entered, the key cannot be changed for this file):\n")
            clrscr()
            if key.lower() == 'exit':
                continue
            
            if len(key) > 32 or len(key) < 5:
                print("Key should be from 5 to 32 characters long!\nLocker creation failed!!\n")
                continue
            
            if '~' in key:
                print("Keys and passwords cannot contain '~'!\nLocker creation failed!!\n")
                continue
            try:    
                newLocker(file, key)
            except FileNotFoundError:
                clrscr()
                print(file)
                print('No such folder exists!\n')
            
        elif choice == '3' or choice.lower() == 'exit':
            sys.exit()
            
        else:
            clrscr()
            print("Invaild input!\n")



if __name__ == '__main__':
    
    main()