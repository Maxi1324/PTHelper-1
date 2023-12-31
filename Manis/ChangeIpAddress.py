name = "Change Ipv4 Addresses"
import re
from lxml import etree
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QWidget,QPushButton

changes = {}

class IPDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.d = {}
        self.initUI()

    def initUI(self):
        global ips
        self.setWindowTitle('IP Addresses')
        self.setFixedSize(700, 450)


        self.ip_widgets = []

        self.addIPs(ips)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        for widget in self.ip_widgets:
            layout.addWidget(widget)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        text = QLabel("Here are all addresses, which where found by double click you can change them\nbtw it simply replaces everywhere the old ip with the new one without checking anything\nso be smart and careful")
        main_layout.addWidget(text)
        main_layout.addWidget(scroll_area)
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet('''
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
        ''')
        ok_button.clicked.connect(self.accept)
        ok_button.setAutoDefault(False)
        main_layout.addWidget(ok_button)

    def addIPs(self, ip_list):
        for ip in ip_list:
            edit = QLineEdit()
            edit.setStyleSheet('''
                background-color: #59EB00;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 20px;
                padding: 10px;
                margin: 2px;
                text-align: center;
            ''')
            edit.setReadOnly(True)
            edit.setText(ip)
            self.d[ip] = {
                "ip": ip,
                "sv": ip
            }
            if(ip in changes):
                self.d[ip]["sv"] = changes[ip]
                edit.setText(changes[ip])
                self.onEditingFinished(edit, ip)

            edit.mousePressEvent = lambda event, editor=edit, ip=ip: self.onDoubleClick(event, editor,ip)
            edit.editingFinished.connect(lambda editor=edit, ip=ip: self.onEditingFinished(editor,ip))

            self.ip_widgets.append(edit)

    def onDoubleClick(self, event, editor, ip):
        editor.setText(self.d[ip]["sv"])
        editor.setReadOnly(False)
        editor.setFocus()

    def onEditingFinished(self, editor, ip):
        self.onReturnPressed(editor, ip)

    def onReturnPressed(self, editor, ip):
        global changes

        self.d[ip]["sv"] = editor.text()
        editor.setVisible(True)
        editor.setReadOnly(True)
        editor.clearFocus()
        if self.d[ip]["sv"] != self.d[ip]["ip"]:
            editor.setText(self.d[ip]["ip"] + "->" + self.d[ip]["sv"])
            changes[self.d[ip]["ip"]] = self.d[ip]["sv"] 
        else:
            editor.setText(self.d[ip]["ip"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = IPDialog()
    dialog.exec_()
    sys.exit(app.exec_())

ips = []


def manipulate(xml):
    xml_text = etree.tostring(xml, encoding="unicode")
    for old, new in changes.items():
        pattern = re.compile(fr'\b{old}\b')
        xml_text = re.sub(pattern,new,xml_text)
    modified_root = etree.fromstring(xml_text)
    return modified_root, None,None

def settings(xml):
    global ips
    xml_text = etree.tostring(xml, encoding="unicode")

    pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = set(re.findall(pattern, xml_text))
    ips = sorted(ips, key=lambda ip: tuple(map(int, ip.split('.'))))

    IPDialog().exec_()
