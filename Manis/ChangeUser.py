from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
import sys

bs = '''
QPushButton {
    background-color: #59EB00;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 20px;
    padding: 10px;
    margin: 1px;
}
QPushButton:hover {
    background-color: #4CAF50;
}
QLineEdit {
    border-radius: 5px;
    border:none;
    font-size: 20px;
    padding: 10px;
    margin: 1px;
}
QLabel {
    font-size: 16px; /* Größere Schriftgröße für Labels */
    margin: 5px;
    color: #333333; /* Textfarbe für Labels */
}
'''

name = "Change User Informations"

user_name = ""
user_email = ""
user_addinfo = ""

class ManipulationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(name)
        self.setFixedSize(500, 350)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Changes the User Informations in the pt file without reseting\n the activity"))

        # Textfelder zur Eingabe der Werte
        name_label = QLabel("User Name:")
        email_label = QLabel("User Email:")
        addinfo_label = QLabel("Additional Info")

        email_label.setStyleSheet(bs)
        name_label.setStyleSheet(bs)
        addinfo_label.setStyleSheet(bs)

        self.name_input = QLineEdit(user_name)
        self.email_input = QLineEdit(user_email)
        self.addinfo_input = QLineEdit(user_addinfo)
        self.name_input.setStyleSheet(bs)
        self.email_input.setStyleSheet(bs)
        self.addinfo_input.setStyleSheet(bs)


        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(addinfo_label)
        layout.addWidget(self.addinfo_input)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(bs)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.name_input.textChanged.connect(self.updateName)
        self.email_input.textChanged.connect(self.updateEmail)
        self.addinfo_input.textChanged.connect(self.updateAddinfo)

        self.setLayout(layout)

    def updateName(self):
        global user_name
        user_name = self.name_input.text()

    def updateEmail(self):
        global user_email
        user_email = self.email_input.text()

    def updateAddinfo(self):
        global user_addinfo
        user_addinfo = self.addinfo_input.text()


def manipulate(xml):
    global user_name
    global user_email
    global user_addinfo

    xml.xpath("//USER_PROFILE")
    for user in xml.xpath("//USER_PROFILE"):
        user.xpath("./NAME")[0].text = user_name
        user.xpath("./EMAIL")[0].text = user_email
        user.xpath("./ADDITIONAL_INFO")[0].text = user_addinfo
    return xml, None, None

first = True

def settings(xml):
    global first
    global user_name
    global user_email
    global user_addinfo
    if(first):
        for user in xml.xpath("//USER_PROFILE"):
            user_name = user.xpath("./NAME")[0].text
            user_email = user.xpath("./EMAIL")[0].text 
            user_addinfo=user.xpath("./ADDITIONAL_INFO")[0].text 
    first = False
    ManipulationDialog().exec()
