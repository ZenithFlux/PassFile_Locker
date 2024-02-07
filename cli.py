import os
import pickle
import sys

from pwinput import pwinput

from tools.locker import *

def newLocker(file, key):
    print('Creating new Locker...')
    locker = Locker(key)

    locker.save(file)

    clrscr()
    openLocker(file, key)
    return


def openLocker(file, key):

    print("Opening the Locker...")
    with open(file, 'rb') as f:
        locker: Locker = pickle.load(f)
    clrscr()

    if locker.unlock(key):
        passmode(locker)
    else:
        raise LockerError('Invalid key')


def passmode(locker: Locker):
    global file

    while True:
        print("---- {0} ----\n--Password Section--".format(os.path.basename(file)))

        if not locker.pwd_dict:
            print('\nNo password added yet...')

        else:
            print("\nSites for which passwords have been found -")
            n=0
            for site in locker.pwd_dict.keys():
                n += 1
                print(f'{n}. {site}')
            del n
            print()

        if locker.pwd_dict:
            print('Enter the number of a site to view/change/delete your password entered for the site.')
        print("Type 'add' to add a new password.\nType 'f' to go into Files Section.\nType 'exit' to close the locker.")
        choice = input().lower()

        if choice == 'f':
            clrscr()
            file_closed = filemode(locker)
            if file_closed == True:
                return
            else:
                continue

        if choice == 'exit':
            return

        elif choice == 'add':
            site = input("Enter a new site name to store password for (Leave empty to cancel): ")
            if not site:
                clrscr()
                continue

            if site in locker.pwd_dict:
                print('Password for this site already exists!\n')
                continue

            newPass = pwinput('Enter the password to store (Leave empty to cancel): ')
            clrscr()

            if not newPass:
                continue

            locker.pwd_dict[site] = newPass
            locker.save(file)
            print('New password added successfully...\n')
            continue

        elif locker.pwd_dict and choice.isnumeric() and int(choice) <= len(locker.pwd_dict.keys()):
            site = list(locker.pwd_dict.keys())[int(choice) - 1]
            password = locker.pwd_dict[site]
            print(f"\nPassword for '{site}' is:\n{password}")
            print("Type 'change' to change this password.")
            print("Type 'delete' to delete this password. Password can't be retrieved once deleted.")
            print("Enter 'b' to go back to site selection menu.")
            choice = input().lower()
            clrscr()

            if choice == 'b':
                clrscr()
                continue

            elif choice == 'change':
                newPass = pwinput("Enter new password (Leave empty to cancel): ")
                clrscr()

                if not newPass:
                    continue

                locker.pwd_dict[site] = newPass
                locker.save(file)
                print('Password updated successfully...\n')
                continue

            elif choice == 'delete':
                del locker.pwd_dict[site]
                locker.save(file)
                print("Password deleted successfully...\n")
                continue

            else:
                print('Invalid input!\n')
                continue

        else:
            clrscr()
            print('Invalid input!\n')
            continue

def filemode(locker: Locker):
    global file
    print("This locker is designed to encrypt important documents. Since encryption is very resource intensive,")
    print("it is not advised to put huge files in the locker. Locker will take more time to encrypt bigger files.\n")
    print("If you want to store large number of files, you can zip those files and store it here.\n")

    while True:
        print("---- {0} ----\n--Files Section --".format(os.path.basename(file)))

        if not locker.files:
            print('\nNo Files found in the locker...')

        else:
            print("\nFollowing files have been found in the locker -")
            n=0
            for filename in locker.files.keys():
                n += 1
                print(f'{n}. {filename}')
            del n
            print()

        if locker.files:
            print('Enter the number of a file to extract/rename/delete that file.')

        print("Type 'add' to add a new file.\nType 'p' to go into Password Section.\nType 'exit' to close the locker.")
        choice = input().lower()

        if choice == 'p':
            clrscr()
            return False

        elif choice == 'add':
            filename = input("Enter path of the file to add (Leave empty to cancel): ")
            if not filename:
                clrscr()
                continue

            try:
                if os.path.getsize(filename) > 2*1024*1024*1024:   # 2 GB = 2*1024*1024*1024 bytes
                    clrscr()
                    print('File too large to add. Size limit per file is set to 2 GB for performance purposes!!\n')
                    continue

                if (os.path.getsize(file) + os.path.getsize(filename)) > 3*1024*1024*1024:
                    clrscr()
                    print("Adding this file will exceed the locker limit (3 GB)!!\n")
                    continue

                with open(filename, 'rb') as f:
                    print("Processing the file...")
                    locker.add_file(os.path.basename(filename), f.read())

            except FileNotFoundError:
                clrscr()
                print(filename)
                print("File not found!\n")
                continue

            locker.save(file)
            clrscr()
            print("File added successfully...\nFrom " + filename +'\n')
            continue

        elif choice == 'exit':
            return True

        elif locker.files and choice.isnumeric() and int(choice) <= len(locker.files):
            filename = list(locker.files.keys())[int(choice) - 1]
            print(f"--- {filename} ---\n")
            print("Type 'extract' to extract the file.\nType 'rename' to rename it.")
            print("Type 'delete' to remove the file from the locker.\nEnter 'b' to go back to the files list.")
            choice = input().lower()

            if choice == "b":
                clrscr()
                continue

            elif choice == "rename":
                newName = input("Enter new name for the file (Leave empty to cancel): ")
                if not newName:
                    clrscr()
                    continue

                print("Renaming the file...")
                locker.rename_file(filename, newName)
                locker.save(file)

                clrscr()
                print("File renamed successfully...\n")
                continue

            elif choice == "delete":
                print("Deleting the file...")
                locker.remove_file(filename)
                locker.save(file)
                clrscr()
                print("File deleted successfully...\n")
                continue

            elif choice == "extract":
                extractpath = input("\nEnter the location to extract the file ('!' to cancel):\n")
                if extractpath == '!':
                    clrscr()
                    continue

                extractpath = os.path.join(extractpath, filename)

                try:
                    print("Extracting the file...")
                    with open(extractpath, 'wb') as f:
                        f.write(locker.get_file(filename))

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

def clrscr():
    os.system('cls')


# Main Program--------------------------------------------------------------------------------------------------

def main():
    global file

    if len(sys.argv) >= 2:
        file = sys.argv[1]
        os.chdir(os.path.dirname(file))
        key = pwinput("Enter key: ")
        clrscr()
        try:
            openLocker(file, key)
        except LockerError:
            print('Invaild key!!')
            input('Press Enter to exit the window...\n')
            sys.exit()
        except:
            print("Something went wrong...")
            input('Press Enter to exit the window...\n')
            sys.exit()
        sys.exit()


    while True:
        print('What should we do?\n1. Open a locker\n2. Create new locker\n3. Exit')
        choice = input('Enter your choice no.: ')

        if choice == '1':
            file = input("Enter path for .lkr file (Leave empty to cancel): ")

            if not file:
                clrscr()
                continue

            if not file.endswith('.lkr'):
                file = file + '.lkr'

            if not os.path.exists(file):
                clrscr()
                print(f'Such file does not exist!\n')
                continue

            key = pwinput("Enter key (Leave empty to cancel): ")
            clrscr()
            if not key:
                clrscr()
                continue

            try:
                openLocker(file, key)
                clrscr()
            except LockerError:
                print('Invaild key!!\n')
                continue

        elif choice == '2':
            file = input("Enter name and path for the new Locker file (Leave empty to cancel): ")
            if not file:
                clrscr()
                continue

            if not file.endswith('.lkr'):
                file = file + '.lkr'

            key = pwinput("Enter key for the locker (Leave empty to cancel): ")
            clrscr()
            if not key:
                continue

            if len(key) > 32 or len(key) < 5:
                print("Key should be from 5 to 32 characters long!\nLocker creation failed!!\n")
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
