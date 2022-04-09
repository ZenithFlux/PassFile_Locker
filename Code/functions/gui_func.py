from Crypto.Random import get_random_bytes
from .encrypter import encrypt, decrypt
from .smallDialogs import *
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QListWidgetItem, QInputDialog, QDialog, QPushButton, QDialogButtonBox
import pickle
import os

'''
Meaning of some common variables used in this file:-
1- path = path of the Locker file opened.
2- data = LockerData object of opened locker.
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
    
def fill_pwList(data, listWidget):    
    for site in data.passwords.keys():
        QListWidgetItem(site, listWidget)
        
def fill_fileList(data, listWidget):    
    for file in data.files.keys():
        QListWidgetItem(file, listWidget)
        
def open_locker(window, LockerWindow):
    path = QFileDialog.getOpenFileName(None, "Select Locker File", "", "Locker Files (*.lkr);;All Files (*)")[0]
    if not path:
        return
    
    while True:    
        key, ok = QInputDialog.getText(None, "Enter password", "Password:", QLineEdit.Password)
        
        if ok:
            with open(path, 'rb') as f:
                data = pickle.load(f)

            if key and decrypt(data.key, key, data.iv) == key:
                changeWindow(window, LockerWindow(path, key, data))
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
        InfoMessageBox("Passwords at least 5 characters long.")
        return
    
    if '~' in key:
        InfoMessageBox("Passwords cannot contain '~'")
        return
    
    if os.path.exists(path):
        confirm_replace = ReplaceConfirmation()
        if confirm_replace.reply != QMessageBox.Yes: return
    
    iv = get_random_bytes(16)
    data = LockerData(encrypt(key, key, iv), iv)
    
    save(path, data)
    changeWindow(window, LockerWindow(path, key, data))
    
# --------------------------Locker Control Functions-------------------------------

def save(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)
        
def pw_veiw(key, data, selected):
    if len(selected) > 1:
        InfoMessageBox("Only one password can be veiwed at a time!")
        return
    
    elif len(selected) == 1:
        site = selected[0].text()
        password = decrypt(data.passwords[site], key, data.iv)
        
        VeiwPasswordDialog(site, password)
    
def pw_delete(path, data, listWidget, selected):
    for site in selected:
        del data.passwords[site.text()]
        listWidget.takeItem(listWidget.row(site))
          
    save(path, data)
    
def file_add(path, key, data, listWidget):
    files = QFileDialog.getOpenFileNames(None, "Select file(s) to encrypt", "", "All Files(*)")

    for filepath in files[0]: 
        filename = filepath.split('/')[-1]
        
        if filename in data.files: _create_list_item = False
        else: _create_list_item = True
        
        if os.path.getsize(filepath) > 2*1024*1024*1024:
            InfoMessageBox(f"{filename}\n\nFile too large to add. Size limit per file is set to 2 GB for better performance!")
        elif (os.path.getsize(path) + os.path.getsize(filepath)) > 3*1024*1024*1024:
            InfoMessageBox(f"{filename}\n\nLocker limit is set to 3GB for performace purposes. Adding this file will exceed the locker limit.")
            
        else:
            with open(filepath, 'rb') as f:
                data.files[filename] = encrypt(None, key, 0, filebytes = f.read())
            
            save(path, data)
            
            if _create_list_item:
                QListWidgetItem(filename, listWidget)
            

def file_rename(path, data, listWidget, selected):
    if len(selected) == 1:
        newName, ok = QInputDialog.getText(None, "Rename File", "File Name:", text = selected[0].text())
        newName = newName.strip()
        
        if ok and newName and newName != selected[0].text():
            data.files[newName] = data.files[selected[0].text()]
            del data.files[selected[0].text()]
            save(path, data)
            
            listWidget.takeItem(listWidget.row(selected[0]))
            QListWidgetItem(newName, listWidget)
    
    elif len(selected) > 1:
        InfoMessageBox("Only one file can be renamed at a time.")
        
        
def file_extract(key, data, selected):
    if selected:
        folder = str(QFileDialog.getExistingDirectory(None, "Select folder to extract file(s) in"))
    else:
        return

    if folder:
        for file in selected:
            filename = file.text()
            filepath = folder + "/" + filename
            
            with open(filepath, 'wb') as f:
                f.write(decrypt(None, key, 0, filebytes = data.files[filename]))
    
    
def file_delete(path, data, listWidget, selected):
    for file in selected:
        del data.files[file.text()]
        listWidget.takeItem(listWidget.row(file))
          
    save(path, data)


class AddPasswordDialog(QDialog):
    def __init__(self, path, key, data, listWidget):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Add new website")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)
        
        self.site_label = QLabel(self)
        self.layout1.addWidget(self.site_label)
        self.site_label.setText("Website Name:")
        
        self.site_textbox = QLineEdit(self)
        self.layout1.addWidget(self.site_textbox)
        self.site_textbox.setFixedWidth(180)
        
        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)
        
        self.password_label = QLabel(self)
        self.layout2.addWidget(self.password_label)
        self.password_label.setText("Password:")
        
        self.password_textbox = QLineEdit(self)
        self.layout2.addWidget(self.password_textbox)
        self.password_textbox.setFixedWidth(180)
        self.password_textbox.setEchoMode(QLineEdit.Password)
        
        self.layout3 = QHBoxLayout()
        self.layout.addLayout(self.layout3)
        
        self.layout3.addStretch(1)
        
        self.show_passwords = QPushButton(self)
        self.layout3.addWidget(self.show_passwords)
        self.show_passwords.setText("Show")
        self.show_passwords.pressed.connect(lambda: self.password_textbox.setEchoMode(QLineEdit.Normal))
        self.show_passwords.released.connect(lambda: self.password_textbox.setEchoMode(QLineEdit.Password))
        
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(lambda: self.ok_clicked(path, key, data, listWidget))
        self.button_box.rejected.connect(self.close)
        self.layout.addWidget(self.button_box)
        
        
        self.setFixedSize(self.minimumSizeHint())
        self.exec()
        
    def ok_clicked(self, path, key, data, listWidget):
        self.site = self.site_textbox.text().strip()
        self.password = self.password_textbox.text()
        
        if not(self.site and self.password):
            InfoMessageBox("Both website name and password are required to complete the action!")
            return
        
        if '~' in self.password:
            InfoMessageBox("Passwords cannot contain '~'")
            return
        
        if not self.site in data.passwords: QListWidgetItem(self.site, listWidget)
        
        data.passwords[self.site] = encrypt(self.password, key, data.iv)
        save(path, data)
        
        self.close()
        
    
class LockerData:
    def __init__(self, key, iv):
        self.key = key
        self.passwords = {}
        self.files = {}
        self.iv = iv