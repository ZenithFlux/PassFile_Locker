from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog
from PyQt5.QtWidgets import QLineEdit, QListWidgetItem, QPushButton, QDialogButtonBox
from PyQt5 import QtCore

from .smallDialogs import *
from .gui_func import show_pressed, show_released
from .locker import Locker


class AddPasswordDialog(QDialog):
    def __init__(self, path, locker: Locker, listWidget):
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
        self.button_box.accepted.connect(lambda: self.ok_clicked(path, locker, listWidget))
        self.button_box.rejected.connect(self.close)
        self.layout.addWidget(self.button_box)


        self.setFixedSize(self.minimumSizeHint())
        self.exec()

    def ok_clicked(self, path, locker: Locker, listWidget):
        self.site = self.site_textbox.text().strip()
        self.password = self.password_textbox.text()

        if not(self.site and self.password):
            InfoMessageBox("Both website name and password are required to complete the action!")
            return

        if not self.site in locker.pwd_dict:
            QListWidgetItem(self.site, listWidget)

        locker.pwd_dict[self.site] = self.password
        locker.save(path)
        self.close()



class ChangePasswordDialog(QDialog):
    def __init__(self, path, locker: Locker, selected):
        if len(selected) > 1:
            InfoMessageBox("Only one password can be changed at a time!")
            return
        elif len(selected) == 0:
            return

        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Change Website Password")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)

        self.layout1.addStretch(1)

        self.site_label = QLabel(self)
        self.layout1.addWidget(self.site_label)
        self.site_label.setText(selected[0].text())
        self.site_label.setFont(QFont(QFont().defaultFamily(), 20))

        self.layout1.addStretch(1)

        self.layout.addSpacing(20)

        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)

        self.password_label = QLabel(self)
        self.layout2.addWidget(self.password_label)
        self.password_label.setText("New Password:")

        self.password_textbox = QLineEdit(self)
        self.layout2.addWidget(self.password_textbox)
        self.password_textbox.setFixedWidth(180)
        self.password_textbox.setEchoMode(QLineEdit.Password)

        self.show_passwords = QPushButton(self)
        self.layout2.addWidget(self.show_passwords)
        self.show_passwords.setText("Show")
        self.show_passwords.pressed.connect(lambda: self.password_textbox.setEchoMode(QLineEdit.Normal))
        self.show_passwords.released.connect(lambda: self.password_textbox.setEchoMode(QLineEdit.Password))


        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(lambda: self.ok_clicked(path, locker, selected))
        self.button_box.rejected.connect(self.close)
        self.layout.addWidget(self.button_box)


        self.setFixedSize(self.minimumSizeHint())
        self.exec()


    def ok_clicked(self, path, locker: Locker, selected):
        new_pwd = self.password_textbox.text()

        if not new_pwd:
            InfoMessageBox("New Password is required to complete the action!")
            return

        locker.pwd_dict[selected[0].text()] = new_pwd
        locker.save(path)
        self.close()



class ChangeLockerPasswordDialog(QDialog):
    def __init__(self, path, locker: Locker):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Change Locker Password")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)

        self.pwd_label = QLabel(self)
        self.layout1.addWidget(self.pwd_label)
        self.pwd_label.setText("New Password:")

        self.pwd_textbox = QLineEdit(self)
        self.layout1.addWidget(self.pwd_textbox)
        self.pwd_textbox.setFixedWidth(180)
        self.pwd_textbox.setPlaceholderText("Minimum 5 characters")
        self.pwd_textbox.setEchoMode(QLineEdit.Password)

        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)

        self.cpwd_label = QLabel(self)
        self.layout2.addWidget(self.cpwd_label)
        self.cpwd_label.setText("Confirm Password:")

        self.cpwd_textbox = QLineEdit(self)
        self.layout2.addWidget(self.cpwd_textbox)
        self.cpwd_textbox.setFixedWidth(180)
        self.cpwd_textbox.setEchoMode(QLineEdit.Password)

        self.layout3 = QHBoxLayout()
        self.layout.addLayout(self.layout3)

        self.layout3.addStretch(1)

        self.show_passwords = QPushButton(self)
        self.layout3.addWidget(self.show_passwords)
        self.show_passwords.setText("Show")
        self.show_passwords.pressed.connect(lambda: show_pressed(self.pwd_textbox, self.cpwd_textbox))
        self.show_passwords.released.connect(lambda: show_released(self.pwd_textbox, self.cpwd_textbox))


        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(lambda: self.ok_clicked(path, locker))
        self.button_box.rejected.connect(self.close)
        self.layout.addWidget(self.button_box)


        self.setFixedSize(self.minimumSizeHint())
        self.exec()


    def ok_clicked(self, path, locker: Locker):
        new_pwd = self.pwd_textbox.text()

        if len(new_pwd) < 5:
            InfoMessageBox("Passwords length should be at least 5 characters.")
            return

        if new_pwd != self.cpwd_textbox.text():
            PasswordMismatch()
            return

        locker.change_password(new_pwd)
        locker.save(path)
        self.close()
