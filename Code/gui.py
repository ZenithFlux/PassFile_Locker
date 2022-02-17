from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QPushButton, QLabel, QListWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from functions.gui_func import *
import sys



class FirstPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassFile Locker")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
        self.open_locker_button = QPushButton(self)
        self.open_locker_button.setText("Open a Locker")
        self.open_locker_button.setFont(QFont('Arial', 10))
        self.open_locker_button.setFixedSize(500, 40)
        self.layout.addWidget(self.open_locker_button)
        self.open_locker_button.clicked.connect(lambda: open_locker(self, LockerWindow))
        
        
        self.or_label = QLabel(self)
        self.or_label.setText("--------OR--------")
        self.or_label.setFont(QFont('Arial', 10))
        self.or_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.or_label)
        
        self.create_locker_button = QPushButton(self)
        self.create_locker_button.setText("Create a New Locker")
        self.create_locker_button.setFont(QFont('Arial', 10))
        self.create_locker_button.setFixedSize(500, 40)
        self.layout.addWidget(self.create_locker_button)
        self.create_locker_button.clicked.connect(lambda: changeWindow(self, NewLockerDialog()))
        
        
        self.setFixedSize(self.minimumSizeHint())
        
        
               
class NewLockerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create a new Locker")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        
        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)
        
        self.location_label = QLabel(self)
        self.layout1.addWidget(self.location_label)
        self.location_label.setText("Location:")
        
        self.location_textbox = QLineEdit(self)
        self.layout1.addWidget(self.location_textbox)
        self.location_textbox.setFixedWidth(180)
        
        self.browse_button = QPushButton(self)
        self.layout1.addWidget(self.browse_button)
        self.browse_button.setText("Browse...")
        self.browse_button.setFixedSize(self.browse_button.minimumSizeHint())
        self.browse_button.clicked.connect(lambda: browse_clicked(self.location_textbox))
        
        
        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)
        
        self.name_label = QLabel(self)
        self.layout2.addWidget(self.name_label)
        self.name_label.setText("Locker Name:")
        
        self.name_textbox = QLineEdit(self)
        self.layout2.addWidget(self.name_textbox)
        self.name_textbox.setFixedWidth(180)
        self.layout2.addSpacing(self.browse_button.width()+7)
        
        
        self.layout3 = QHBoxLayout()
        self.layout.addLayout(self.layout3)
        
        self.password_label = QLabel(self)
        self.layout3.addWidget(self.password_label)
        self.password_label.setText("Password:")
        
        self.password_textbox = QLineEdit(self)
        self.layout3.addWidget(self.password_textbox)
        self.password_textbox.setFixedWidth(180)
        self.password_textbox.setPlaceholderText("At least 5 characters required")
        self.password_textbox.setMaxLength(32)
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.layout3.addSpacing(self.browse_button.width()+7)

        
        self.layout4 = QHBoxLayout()
        self.layout.addLayout(self.layout4)
        
        self.cpassword_label = QLabel(self)
        self.layout4.addWidget(self.cpassword_label)
        self.cpassword_label.setText("Confirm Password:")
        
        self.cpassword_textbox = QLineEdit(self)
        self.layout4.addWidget(self.cpassword_textbox)
        self.cpassword_textbox.setMaxLength(32)
        self.cpassword_textbox.setFixedWidth(180)
        self.cpassword_textbox.setEchoMode(QLineEdit.Password)
        
        self.show_passwords = QPushButton(self)
        self.layout4.addWidget(self.show_passwords)
        self.show_passwords.setText("Show")
        self.show_passwords.setFixedSize(self.browse_button.size())
        self.show_passwords.pressed.connect(lambda: show_pressed(self.password_textbox, self.cpassword_textbox))
        self.show_passwords.released.connect(lambda: show_released(self.password_textbox, self.cpassword_textbox))
        
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.ok_clicked)
        self.button_box.rejected.connect(lambda: changeWindow(self, FirstPage()))
        self.layout.addWidget(self.button_box)
        
        
        self.setFixedSize(self.minimumSizeHint())
        
    def ok_clicked(self):
        if not self.location_textbox.text().strip():
            InfoMessageBox("It is required to select some location for Locker!")
            return
        
        if not os.path.exists(self.location_textbox.text().strip()):
            InvaildLocationBox()
            return
            
        if not self.name_textbox.text().strip():
            InfoMessageBox("Please enter a name for the Locker!")
            return
        
        self._lockerpath = self.location_textbox.text() + "/" + self.name_textbox.text()
        createNewLocker(self._lockerpath, (self.password_textbox.text(), self.cpassword_textbox.text()), self, LockerWindow)

# Size of the List Boxes in the LockerWindow
SIZEX = 230
SIZEY = 400

class LockerWindow(QWidget):    
    def __init__(self, path, key, data):
        super().__init__()
        self.setWindowTitle(path.split('/')[-1].split('\\')[-1] + " - PassFile Locker")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)
        self.layout = QHBoxLayout()
        self.base_layout.addLayout(self.layout)
        self.initUI(path, key, data)
    
    
        
    def initUI(self, path, key, data):
        # From here, layout12 would mean layout2 of layout1
        self.layout1 = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        
        self.pw_label = QLabel(self)
        self.layout1.addWidget(self.pw_label)
        self.pw_label.setText("Passwords:")
        
        self.layout11 = QHBoxLayout()
        self.layout1.addLayout(self.layout11)
        
        self.pw_list = QListWidget(self)
        self.layout11.addWidget(self.pw_list)
        self.pw_list.setFixedSize(SIZEX, SIZEY)
        self.pw_list.setSortingEnabled(True)
        self.pw_list.setSelectionMode(QListWidget.ExtendedSelection)
        fill_pwList(data, self.pw_list)
        
        self.layout111 = QVBoxLayout()
        self.layout11.addLayout(self.layout111)
        self.layout111.setSpacing(25)
        
        
        self.pwAdd = QPushButton(self)
        self.layout111.addWidget(self.pwAdd)
        self.pwAdd.setText("Add")
        self.pwAdd.clicked.connect(lambda: AddPasswordDialog(path, key, data, self.pw_list))
        
        self.pwView = QPushButton(self)
        self.layout111.addWidget(self.pwView)
        self.pwView.setText("View")
        self.pwView.clicked.connect(lambda: pw_veiw(key, data, self.pw_list.selectedItems()))
    
        self.pwDelete = QPushButton(self)
        self.layout111.addWidget(self.pwDelete)
        self.pwDelete.setText("Delete")
        self.pwDelete.clicked.connect(lambda: DeleteConfirmation("password", path, data, self))
        
        self.layout111.addStretch(1)
        
        self.layout.addSpacing(100)
        
        
        self.layout2 = QVBoxLayout()
        self.layout.addLayout(self.layout2)
        
        self.file_label = QLabel(self)
        self.layout2.addWidget(self.file_label)
        self.file_label.setText("Files:")
        
        self.layout21 = QHBoxLayout()
        self.layout2.addLayout(self.layout21)
        
        self.file_list = QListWidget(self)
        self.layout21.addWidget(self.file_list)
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setSortingEnabled(True)
        self.file_list.setFixedSize(SIZEX, SIZEY)
        fill_fileList(data, self.file_list)
        
        self.layout211 = QVBoxLayout()
        self.layout21.addLayout(self.layout211)
        self.layout211.setSpacing(25)
        
        
        self.fileAdd = QPushButton(self)
        self.layout211.addWidget(self.fileAdd)
        self.fileAdd.setText("Add")
        self.fileAdd.clicked.connect(lambda: file_add(path, key, data, self.file_list))
        
        self.fileRename = QPushButton(self)
        self.layout211.addWidget(self.fileRename)
        self.fileRename.setText("Rename")
        self.fileRename.clicked.connect(lambda: file_rename(path, data, self.file_list, self.file_list.selectedItems()))
        
        self.fileExtract = QPushButton(self)
        self.layout211.addWidget(self.fileExtract)
        self.fileExtract.setText("Extract")
        self.fileExtract.clicked.connect(lambda: file_extract(key, data, self.file_list.selectedItems()))
        
        self.fileDelete = QPushButton(self)
        self.layout211.addWidget(self.fileDelete)
        self.fileDelete.setText("Delete")
        self.fileDelete.clicked.connect(lambda: DeleteConfirmation("file", path, data, self))
        
                
        self.layout211.addStretch(1)
        
        self.base_layout.addSpacing(30)
        
        self.button_box = QDialogButtonBox(self)
        self.base_layout.addWidget(self.button_box)
        self.close_locker_button = QPushButton(self)
        self.close_locker_button.setText("Close Locker")
        self.button_box.addButton(self.close_locker_button, QDialogButtonBox.RejectRole)
        if len(sys.argv) >= 2:
            self.button_box.rejected.connect(self.close)
        else:
            self.button_box.rejected.connect(lambda: changeWindow(self, FirstPage()))
        
        
        self.setFixedSize(self.minimumSizeHint())
  
  
class DeleteConfirmation(QMessageBox):
    def __init__(self, for_which, path, data, window):
        super().__init__()
        self.setWindowTitle("Confirm Delete")
        self.setIcon(QMessageBox.Warning)
        self.setText(f"Do you really wish to delete the selected {for_which}(s) from this Locker?")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if (window.file_list.selectedItems() and for_which == "file") or (window.pw_list.selectedItems() and for_which == "password"):
            self.show()
            self.pressed = self.exec()
            
            if for_which == "password" and self.pressed == QMessageBox.Yes:
                pw_delete(path, data, window.pw_list, window.pw_list.selectedItems())
            elif for_which == "file" and self.pressed == QMessageBox.Yes:
                file_delete(path, data, window.file_list, window.file_list.selectedItems())
                
            elif self.pressed == QMessageBox.No:
                pass
            
        else:
            self.close()
            

def main():
    
    # Following code will initiate the app if app is opened using a locker file
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("icon.ico"))
        
        while True:    
            key, ok = QInputDialog.getText(None, "Enter password", "Password:", QLineEdit.Password)
        
            if ok:
                with open(path, 'rb') as f:
                    data = pickle.load(f)

                if key and decrypt(data.key, key, data.iv) == key:
                    win = LockerWindow(path, key, data)
                    win.show()
                    sys.exit(app.exec_())
                    
                else:
                    WrongPassword()
                    continue
            else:
                sys.exit() 
    
    # Following code will initiate the app if app is opened directly from .exe
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    win = FirstPage()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()