import pickle
import os

from PyQt5.QtWidgets import QFileDialog, QLineEdit, QListWidgetItem, QInputDialog

from .smallDialogs import *
from . import dialogs
from .locker import Locker


'''
Meaning of some common variables used in this file:-
1- path = path of the Locker file opened.
2- locker = Locker object of opened locker.
3- selected = list of selected QListWidgetItem in corresponding listWidget.
'''


# ---------------------------GUI functions----------------------------------
def changeWindow(prev, next):
    prev.close()
    next.show()

def browse_clicked(textbox):
    path = str(QFileDialog.getExistingDirectory(None, "Select Location for Locker"))

    textbox.setText(path)

def show_pressed(textbox1, textbox2):
    textbox1.setEchoMode(QLineEdit.Normal)
    textbox2.setEchoMode(QLineEdit.Normal)

def show_released(textbox1, textbox2):
    textbox1.setEchoMode(QLineEdit.Password)
    textbox2.setEchoMode(QLineEdit.Password)

def fill_pwList(locker: Locker, listWidget):
    for site in locker.pwd_dict.keys():
        QListWidgetItem(site, listWidget)

def fill_fileList(locker: Locker, listWidget):
    for file in locker.files.keys():
        QListWidgetItem(file, listWidget)

def open_locker(window, LockerWindow):
    path = QFileDialog.getOpenFileName(None, "Select Locker File", "", "Locker Files (*.lkr);;All Files (*)")[0]
    if not path:
        return

    while True:
        key, ok = QInputDialog.getText(None, "Enter password", "Password:", QLineEdit.Password)

        if ok:
            with open(path, 'rb') as f:
                locker: Locker = pickle.load(f)

            if key and locker.unlock(key):
                changeWindow(window, LockerWindow(path, locker))
                break

            else:
                WrongPassword()
        else:
            break

def createNewLocker(path, keypair, window, LockerWindow):
    if keypair[0] != keypair[1]:
        PasswordMismatch()
        return

    if not path.endswith('.lkr'):
        path = path + '.lkr'

    key = keypair[0]

    if len(key) > 32 or len(key) < 5:
        InfoMessageBox("Passwords length should be between 5 to 32 characters.")
        return

    if os.path.exists(path):
        confirm_replace = ReplaceConfirmation()
        if confirm_replace.reply != QMessageBox.Yes: return

    locker = Locker(key)

    locker.save(path)
    changeWindow(window, LockerWindow(path, key, locker))


# --------------------------Locker Control Functions-------------------------------

def pw_veiw(locker: Locker, selected):
    if len(selected) > 1:
        InfoMessageBox("Only one password can be veiwed at a time!")
        return

    elif len(selected) == 1:
        site = selected[0].text()
        dialogs.ViewPasswordDialog(site, locker.pwd_dict[site])


def pw_delete(path, locker: Locker, listWidget, selected):
    for site in selected:
        del locker.pwd_dict[site.text()]
        listWidget.takeItem(listWidget.row(site))

    locker.save(path)


def file_add(path, locker: Locker, listWidget):
    files = QFileDialog.getOpenFileNames(None, "Select file(s) to encrypt", "", "All Files(*)")

    for filepath in files[0]:
        filename = os.path.basename(filepath)

        if filename in locker.files: _create_list_item = False
        else: _create_list_item = True

        if os.path.getsize(filepath) > 2*1024*1024*1024:
            InfoMessageBox(f"{filename}\n\nFile too large to add. Size limit per file is set to 2 GB for better performance!")
        elif (os.path.getsize(path) + os.path.getsize(filepath)) > 3*1024*1024*1024:
            InfoMessageBox(f"{filename}\n\nLocker limit is set to 3GB for performace purposes. Adding this file will exceed the locker limit.")

        else:
            with open(filepath, 'rb') as f:
                locker.add_file(filename, f.read())

            locker.save(path)

            if _create_list_item:
                QListWidgetItem(filename, listWidget)


def file_rename(path, locker: Locker, listWidget, selected):
    if len(selected) == 1:
        newName, ok = QInputDialog.getText(None, "Rename File", "File Name:", text = selected[0].text())
        newName = newName.strip()

        if ok and newName and newName != selected[0].text():
            locker.rename_file(selected[0].text(), newName)
            locker.save(path)

            listWidget.takeItem(listWidget.row(selected[0]))
            QListWidgetItem(newName, listWidget)

    elif len(selected) > 1:
        InfoMessageBox("Only one file can be renamed at a time.")


def file_extract(locker: Locker, selected):
    if selected:
        folder = str(QFileDialog.getExistingDirectory(None, "Select folder to extract file(s) in"))
    else:
        return

    if folder:
        for file in selected:
            filename = file.text()
            filepath = os.path.join(folder, filename)

            with open(filepath, 'wb') as f:
                f.write(locker.get_file(filename))


def file_delete(path, locker: Locker, listWidget, selected):
    for file in selected:
        locker.remove_file(file.text())
        listWidget.takeItem(listWidget.row(file))

    locker.save(path)
