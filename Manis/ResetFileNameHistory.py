from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QLabel, QGridLayout
from lxml import etree
class ListDialog(QDialog):
    def __init__(self, elements, max_elements=5):
        super().__init__()
        self.setWindowTitle('List Dialog')
        self.layout = QVBoxLayout()
        self.setFixedSize(700, 350)

        # Label hinzufügen
        label = QLabel("PacketTracer logs every location the file was opened here you\ncan delete the history or modify it")
        label.setStyleSheet('''
            font-size: 16px; /* Textgröße anpassen */
            padding: 10px; /* Innenabstand hinzufügen */
        ''')
        self.layout.addWidget(label)

        # ListWidget für die Elemente
        self.list_widget = QListWidget()
        self.list_widget.addItems(elements)
        self.list_widget.setStyleSheet('''
            border-radius: 5px; /* Abgerundeter Radius von 5px */
            font-size: 15px;
        ''')

        # Schaltflächen-Layout erstellen
        button_layout = QGridLayout()
        add_button = QPushButton('Hinzufügen')
        remove_button = QPushButton('Entfernen')
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.close)

        add_button.setStyleSheet('''
            background-color: #59EB00; /* Hintergrundfarbe nur für Buttons */
            color: white; /* Textfarbe nur für Buttons */
            border: none;
            border-radius: 5px; /* Abgerundeter Radius von 5px */
            font-size: 20px;
            padding: 10px;
            margin: 5px;
        ''')

        remove_button.setStyleSheet('''
            background-color: #59EB00; /* Hintergrundfarbe nur für Buttons */
            color: white; /* Textfarbe nur für Buttons */
            border: none;
            border-radius: 5px; /* Abgerundeter Radius von 5px */
            font-size: 20px;
            padding: 10px;
            margin: 5px;
        ''')

        ok_button.setStyleSheet('''
            background-color: #59EB00; /* Hintergrundfarbe nur für Buttons */
            color: white; /* Textfarbe nur für Buttons */
            border: none;
            border-radius: 5px; /* Abgerundeter Radius von 5px */
            font-size: 20px;
            padding: 10px;
            margin: 5px;
        ''')

        # Schaltflächen dem Layout hinzufügen
        button_layout.addWidget(add_button, 0, 0)
        button_layout.addWidget(remove_button, 0, 1)
        button_layout.addWidget(ok_button, 1, 0, 1, 2)

        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)

        add_button.clicked.connect(self.add_element)
        remove_button.clicked.connect(self.remove_element)

        self.setLayout(self.layout)

        self.max_elements = max_elements

    def add_element(self):
        text, ok = QInputDialog.getText(self, 'Element hinzufügen', 'Geben Sie einen neuen Wert ein:')
        if ok and text:
            self.list_widget.addItem(text)
        global elements
        elements = self.get_elements()
        

    def remove_element(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            for item in selected_items:
                self.list_widget.takeItem(self.list_widget.row(item))
        global elements
        elements = self.get_elements()

    def get_elements(self):
        items = []
        for index in range(self.list_widget.count()):
            items.append(self.list_widget.item(index).text())
        return items

if __name__ == '__main__':
    app = QApplication([])
    elements = ['Element 1', 'Element 2', 'Element 3','Element 1', 'Element 2', 'Element 3','Element 1', 'Element 2', 'Element 3']
    max_elements = 5
    dialog = ListDialog(elements, max_elements)
    dialog.exec_()

name = "Change File Name History"

def manipulate(xml):
    global elements
    recent_files_elements = xml.xpath("//RECENT_FILES")
    
    for recent_files_element in recent_files_elements:
        for file_element in recent_files_element.xpath("./FILE"):
            recent_files_element.remove(file_element)
        
        for element_text in elements:
            new_file_element = etree.Element("FILE")
            new_file_element.text = element_text
            recent_files_element.append(new_file_element)
    
    return xml, None, None

first = True
elements = []

def settings(xml):
    global first 
    global elements
    if(first):
        recent_files_elements = xml.xpath("//RECENT_FILES")
        files_count = {}
        for recent_files in recent_files_elements:
            file_count = len(recent_files.xpath("./FILE"))
            files_count[recent_files] = file_count

        most_files_element = max(files_count, key=files_count.get)
        files =  most_files_element.xpath("./FILE")
        elements = (file.text for file in files)
    first = False
    ListDialog(elements, 0).exec()