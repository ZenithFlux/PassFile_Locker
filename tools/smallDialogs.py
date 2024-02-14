from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog
from PyQt5 import QtCore

class PasswordMismatch(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Mismatch")
        self.setIcon(QMessageBox.Critical)
        self.setText("Passwords don't match!!")
        self.setStandardButtons(QMessageBox.Ok)
        self.show()
        self.exec()

class ReplaceConfirmation(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Replace File")
        self.setIcon(QMessageBox.Warning)
        self.setText("File with same name already exists. Do you want to replace the old file?")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.show()
        self.reply = self.exec()

class InvaildLocationBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invaild Location")
        self.setIcon(QMessageBox.Critical)
        self.setText("Location entered does not exist!!")
        self.setStandardButtons(QMessageBox.Ok)
        self.show()
        self.exec()

class InfoMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Information")
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)
        self.show()
        self.exec()

class CriticalMessageBox(QMessageBox):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)
        self.show()
        self.exec()


class ViewPasswordDialog(QDialog):
    def __init__(self, site, password):
        super().__init__()
        self.setWindowTitle("View Password")
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
        self.site_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.layout1.addStretch(1)

        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)

        self.layout2.addStretch(1)

        self.pass_label = QLabel(self)
        self.layout2.addWidget(self.pass_label)
        self.pass_label.setText("Password:")
        self.pass_label.setFont(QFont(QFont().defaultFamily(), 10))

        self.pwd = QLabel(self)
        self.layout2.addWidget(self.pwd)
        self.pwd.setText(password)
        self.pwd.setFont(QFont(QFont().defaultFamily(), 10))
        self.pwd.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.layout2.addStretch(1)


        self.setFixedSize(max(self.minimumSizeHint().width(), 400), max(self.minimumSizeHint().height(), 200))
        # So that size is never less than 400 x 200

        self.exec()
