from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog
from PyQt5.QtWidgets import QLineEdit, QListWidgetItem, QDialog, QPushButton, QDialogButtonBox
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

from .smallDialogs import *
from .encrypter import encrypt
from . import gui_func as f

class ViewPasswordDialog(QDialog):
    def __init__(self, site, password):
        super().__init__()
        self.setWindowTitle("Decrypted Password")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)
        
        self.layout1.addStretch(1)
        
        self.site_label = QLabel(self)
        self.layout1.addWidget(self.site_label)
        self.site_label.setText(site)
        self.site_label.setFont(QFont(QFont().defaultFamily(), 20))
        
        self.layout1.addStretch(1)
        
        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)
        
        self.layout2.addStretch(1)
        
        self.pass_label = QLabel(self)
        self.layout2.addWidget(self.pass_label)
        self.pass_label.setText(f"Password: {password}")
        self.pass_label.setFont(QFont(QFont().defaultFamily(), 10))
        
        self.layout2.addStretch(1)
        
        
        self.setFixedSize(max(self.minimumSizeHint().width(), 400), max(self.minimumSizeHint().height(), 200))
        # So that size is never less than 400 x 200
        
        self.exec()    
       
        
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
        f.save(path, data)
        
        self.close()