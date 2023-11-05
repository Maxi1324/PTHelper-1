name = "Change OSPF Areas"
import re
from lxml import etree
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QWidget,QPushButton

changes = {}

class IPDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global ips
        self.setWindowTitle('Change OSPF Area')
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

        text = QLabel("Here you can change all ospf areas to another")
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
        global changes

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

            val = re.findall(r"\d", ip)[1]

            if(ip not in changes):
                changes[ip] = {
                    "ip": val,
                    "sv": val
                }
            edit.setText(changes[ip]["sv"])
            self.onReturnPressed(edit, ip)

            edit.mousePressEvent = lambda event, editor=edit, ip=ip: self.onDoubleClick(event, editor,ip)
            edit.editingFinished.connect(lambda editor=edit, ip=ip: self.onEditingFinished(editor,ip))

            self.ip_widgets.append(edit)



    def onDoubleClick(self, event, editor, ip):
        global changes
        editor.setText(changes[ip]["sv"])
        editor.setReadOnly(False)
        editor.setFocus()

    def onEditingFinished(self, editor, ip):
        self.onReturnPressed(editor, ip)

    def onReturnPressed(self, editor, ip):
        global changes

        changes[ip]["sv"] = editor.text()
        editor.setVisible(True)
        editor.setReadOnly(True)
        editor.clearFocus()
        if changes[ip]["sv"] != changes[ip]["ip"]:
            editor.setText("OSPF Area changed from {} to {}".format(changes[ip]["ip"], changes[ip]["sv"]))
            changes[changes[ip]["ip"]] = changes[ip]["sv"] 
        else:
            editor.setText("OSPF Area: {}".format(changes[ip]["ip"]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = IPDialog()
    dialog.exec_()
    sys.exit(app.exec_())

ips = []

def manipulate(xml):
    global changes

    xml_text = etree.tostring(xml, encoding="unicode")
    for key, v in changes.items():
        if not isinstance(v,str):
            newVal = v["sv"]
            replaceStr = key[:-1] + newVal
            xml_text = xml_text.replace(key, replaceStr)

    modified_root = etree.fromstring(xml_text)
    return modified_root, None,None

def settings(xml):
    global ips
    xml_text = etree.tostring(xml, encoding="unicode")

    pattern = re.compile(r'ospf \d+ area \d+')
    ips = set(re.findall(pattern, xml_text))
    ips = sorted(ips)

    IPDialog().exec_()

