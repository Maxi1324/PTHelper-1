from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QListWidget, QSlider, QPushButton
import os
import importlib


class ManipulationDialog(QDialog):
    def __init__(self,p):
        super().__init__()
        self.p = p
        self.setWindowTitle("Benutzerdefinierter Dialog")
        self.setFixedSize(600,400)
        layout = QVBoxLayout()

        self.manis = self.load_manis()

        list_widget = QListWidget()
        self.list_widget = list_widget
        list_widget.setStyleSheet('''
            QListWidget {
                background-color: #59EB00; /* Hintergrundfarbe der Liste */
                border: 1px solid #ccc; /* Rahmen */
                border-radius: 5px; /* Abgerundete Ecken */
                color: #000; /* Textfarbe der Liste */
                font-size: 20px;

            }

            QListWidget::item {
                padding: 10px; /* Innenabstand der Liste */
                background-color:#ffffff; /* Hintergrundfarbe der Elemente */
                margin:4px;
                border: none; /* Kein Rahmen */ 
                border-radius: 3px; /* Abgerundete Ecken */
                font-size: 20px;
            }

            QListWidget::item::selected{
                background : #d4d4d4; /* Hintergrundfarbe des ausgewählten Elements */
                color: black; /* Textfarbe des ausgewählten Elements */
            }
        ''')
        for i in self.manis:
            list_widget.addItem(i.name)
        layout.addWidget(list_widget)


        ok_button = QPushButton("OK")
        ok_button.setStyleSheet('''
          QPushButton {
                background-color: #59EB00; /* Hintergrundfarbe des Buttons */
                color: white; /* Textfarbe */
                border: none; /* Kein Rahmen */
                border-radius: 5px; /* Abgerundete Ecken */
                font-size: 20px;
                padding: 10px;
                margin: 1px;
            }
            QPushButton:hover {
                background-color: #4CAF50; /* Hintergrundfarbe beim Überfahren */
            }
        ''')
        ok_button.clicked.connect(self.close)  
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def close(self):
        v = next((x for x in self.manis if x.name == self.list_widget.currentItem().text()), None)
        self.p.addMani(v)
        self.accept()
        v.settings(self.p.xml)

    def load_manis(self):
        manis = []
        import sys
        if hasattr(sys, '_MEIPASS'):
            p = os.path.join(sys._MEIPASS, "Manis")
        else:
            p = os.path.join(os.getcwd(), "Manis")
        ld = os.listdir(p)
        for datei in ld:
            if datei.endswith(".py"):
                modulname = datei[:-3]  # Entferne die Dateiendung (.py)
                modul = importlib.import_module(f"Manis.{modulname}")

                if(modul not in self.p.mains):
                    manis.append(modul)

        return manis


