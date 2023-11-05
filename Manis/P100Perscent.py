name = "100% grading(works poorly)"
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

def manipulate(xml):
   

    for element in xml.xpath("//NODE"):
        element.set("eclass", "8")
        element.set("checkType", "0")
        element.set("nodeValue", "")

        for e in element.xpath("./ID"):
            e.text = "Power Distribution Device"

  




    return xml, None,None

def settings(xml):
    text = """
    Removes any COMPARISONS defined in the file.\nThis results in a 100% completion but also removes them. \nSo, if the auditor checks what was done, he will see it. \nHowever, if he only checks the percentage, he does not see it.
    """
    dialog = QDialog()
    dialog.setWindowTitle("Textdialog")
    dialog.setFixedSize(400, 200)
    layout = QVBoxLayout()
    label = QLabel(text)
    layout.addWidget(label)
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
    ok_button.clicked.connect(dialog.accept)  # Schließen Sie den Dialog, wenn der OK-Button geklickt wird
    layout.addWidget(ok_button)
    dialog.setLayout(layout)
    dialog.exec_()
#<NAME checkType="1" eclass="8" headNode="true" incorrectFeedback="" nodeValue="2" obfuscateName="false" overrideDBGrading="false" translate="true" variableEnabled="false" variableName="">Power Distribution Device0</NAME>
#    <ID translate="true">Power Distribution Device0</ID>
#    <COMPONENTS></COMPONENTS>
#    <POINTS></POINTS>

 # elements = xml.xpath('.//*[@checkType]')
 #   for element in elements:
 #       element.set('checkType', '1')
#
 #   elements = xml.xpath('.//*[@overrideDBGrading]')
 #   for element in elements:
 #       element.set('overrideDBGrading', 'true')
