from PyQt5.QtWidgets import QMessageBox

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
        
class WrongPassword(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wrong Password")
        self.setIcon(QMessageBox.Critical)
        self.setText("Password entered for the Locker is wrong!!")
        self.setStandardButtons(QMessageBox.Ok)
        self.show()
        self.exec()