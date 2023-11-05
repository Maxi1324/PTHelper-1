print("starting...takes a while")
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget,QStackedLayout,QGridLayout
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Graph import Graph
from ManipulationDialog import ManipulationDialog
from PkaHelper import PkaHelper
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea
import shutil
from lxml import etree
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QListWidget, QPushButton, QMenu, QAction
from PyQt5.QtWidgets import QApplication, QMessageBox



class ModernUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pkahelper = PkaHelper()
        self.graph = Graph()
        self.mains = []
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #61FF00;")
        self.setWindowTitle("PKA Helper")
        self.setFixedSize(900, 600)
        self.centerWindow()
        self.setStyleSheet("background-color: white; color: black;")
        self.setFont(QFont("Roboto", 12) )
     
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.page1())


     
        central_widget.setLayout(self.stacked_layout)

    def showGraph(self):
        w = QWidget(self)
        w.setFixedSize(int(self.width()/2),int(self.height()-100))
        layout = QVBoxLayout(w)
        w.setLayout(layout)
        layout.addWidget(self.graph.generate_graph(self.xml))
        return w

    def page1(self):
        label = self.banner()

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignHCenter)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.fileIcon())

        page1_w = QWidget()
        page1_w.setStyleSheet("background-color: white; color: black;")
        page1 = QVBoxLayout()
        page1.setContentsMargins(0, 0, 0, 0)
        page1.addWidget(label)
        page1.setAlignment(Qt.AlignTop)
        page1_w.setLayout(page1)
        v_layout.addLayout(h_layout)
        page1.addLayout(v_layout)
        return page1_w

    def banner(self):
        label = QLabel("PKA Helper", self)
        label.setAlignment(Qt.AlignCenter)  
        label.setStyleSheet("font-size: 24px; color: white; background-color: #61FF00;text-align: left;")  # Stil definieren
        label.setFixedSize(self.width(),50)  
        label.setContentsMargins(0, 0, 0, 0)

        label.mousePressEvent = self.showCert

        return label

    def showCert(self, event):
        cert_content = '''HIK2vvc5dWNlpqOKYobwukCQUSQon6syKodEJWF7uUmUGj7SQGwBbEF18hdxhESX4I/8plH8aicbJfemhsii6tz1BU/DS6h8Q1vT+vNlnnzgNb+T1QPqLDWpIHbm+NGIz23dlDweVyZkOXEWHaCKD0LswJNdvfJjkFL3ObyX/dLPdbdeCm3ALrs+/Vcp1DynJ8eZauUIHIQ5VF0Qq4+5aJoOUw/repOLjYXVwWfco5l2pUaFo2Ajvww7cvTZSYOdv4GiR33q05nOr/VrTg4ypu4ne/aLWNRhqXP71CgMWmukIacfD7HuHL24pcY7UAe8/uutOUOaDDYoDRLV5HntKtvZCgp3SFNwGlrMzN4/7pTz/YEM+mWp7EZSjtOuFx5jDw1CQfAbK7O1PF9XXQkWpQ5BwQazczduLz1dwBhiNXm4gDhZJ4zHpx9MnBJANlARWqbPtYRRJguQ3SGlSVmoE1QUrFM50fjkzBIEAXKFG7EY1d0031Y8rbB6rlAPIDO+FmubDsWAdUcNcPTF6Ftzuus4Kybe0l2Fzh7zgt7xaRDTm7rogDWyEbPinEhI1kR7CofWyIh0qdn5W27CsXAwBJ1ryKi24MOowE7UA2uBoqqGqqLpzWQotMqT7yf9zO3ePfIrC0H6fC9f3Xm8INrlWaryjbFReAiSTRS8/MmvmPI='''
        clipboard = QApplication.clipboard()
        clipboard.setText(cert_content)

        msg = QMessageBox()
        msg.setWindowTitle("Zertifikat")
        msg.setText("string copied to clipboard you know what to do, if not, just ignore this")
        msg.setIcon(QMessageBox.Information)
        msg.addButton(QMessageBox.Ok)
        msg.exec()
    def page2(self):
        page2_w = QWidget()
        list_v= QVBoxLayout()
        grid_w = QWidget()
        grid = QGridLayout()

        list_v.setContentsMargins(0, 0, 0, 0)
        list_v.addWidget(self.banner())
        list_v.addWidget(grid_w)

        grid_w.setLayout(grid)
        grid.addWidget(self.showGraph(),0,0)
        grid.addWidget(self.side(),0,1)

        page2_w.setLayout(list_v)
        return page2_w

    def modMan(self):
        central_widget = QWidget()  # Erstelle das zentrale Widget einmal

        layout = QVBoxLayout()
        
        # Füge einige Widgets zum Layout hinzu
       

        # Lege das Layout im zentralen Widget fest
        central_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(central_widget)
        scroll_area.setAlignment(Qt.AlignTop)
        scroll_area.setFixedSize(int(self.width()/2)-50,int(self.height()-300))
        self.modL = layout

        scroll_area.setStyleSheet('''
         QScrollArea {
            background: #61FF00; /* Hintergrundfarbe */
            border: 1px solid #000000; /* Schwarzer Rahmen */
            border-radius: 2px; /* Abgerundete Ecken */
        }
        QScrollBar:vertical {
            background: transparent; /* Transparente vertikale Scrollleiste */
            width: 10px; /* Breite der Scrollleiste */
        }
        QScrollBar::handle:vertical {
            background: #61FF00; /* Blauer Hintergrund des Scrollbalken-Griffs */
            border: 2px solid #61FF00; /* Blauer Rand um den Griff */
            border-radius: 4px; /* Abgerundete Ecken für den Griff */
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: transparent; /* Unsichtbare Schaltflächen für Scrollleiste */
        }
        ''')

        return scroll_area

    def side(self):
        widget = QWidget()
        vlayout = QVBoxLayout()
        widget.setLayout(vlayout)
        vlayout.addWidget(self.modMan())

            

        vlayout.addWidget(self.getButton("Add Manipulation", self.showManipulation))
        vlayout.addWidget(self.getButton("Export",self.export))
        return widget

    def getButton(self, text, function = None):
        button = QPushButton(text)
       # button.clicked.connect(function)
        button.setStyleSheet('''
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
        if function is not None:
            button.clicked.connect(function)
        return button

    def showManipulation(self):
        ManipulationDialog(self).exec_()

    def fileIcon(self):
        label = QLabel(self)
        import sys
        p = ""
        if hasattr(sys, '_MEIPASS'):
            p = sys._MEIPASS
        else:
            p = os.getcwd()
        pixmap = QPixmap(p+"\\FileIcon.png") 
        label.setPixmap(pixmap)

        label.setScaledContents(True) 
        label.setCursor(Qt.PointingHandCursor) 
        label.setMargin(120)
        label.setFixedSize(550, 550)  
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.mousePressEvent = self.openFileDialog  
        return label

    def centerWindow(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def openFileDialog(self,a):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Packet Tracer Files (*.pka *.pkt)", options=options)
       
        if file_name:
            self.xml = self.pkahelper.decrypt(file_name,file_name.split(".")[-1])
            self.fileend = file_name.split(".")[-1]
            self.stacked_layout.addWidget(self.page2())
            self.stacked_layout.setCurrentIndex(1)

    def addMani(self, mani):

        self.mains.append(mani)
        b = self.getButton(mani.name,lambda: mani.settings(self.xml))
        self.modL.addWidget(b)
        context_menu = QMenu(b)
        right_click_action = QAction("remove", b)
        context_menu.addAction(right_click_action)
        right_click_action.triggered.connect(lambda: self.removeMani(mani,b))
        b.setContextMenuPolicy(Qt.CustomContextMenu)
        b.customContextMenuRequested.connect(self.show_context_menu)

    def removeMani(self, mani, b):
        self.mains.remove(mani)
        self.modL.removeWidget(b)
        b.deleteLater()
        del b
        self.modL.update()

    def show_context_menu(self, pos):
        button = self.sender()
        if button:
            context_menu = button.parent().findChild(QMenu)
            if context_menu:
                context_menu.exec_(button.mapToGlobal(pos))

    def export(self):
        xml2 = self.xml
        end = self.fileend
        for m in self.mains:
            xml, end2, rep = m.manipulate(xml2)
            if end2 is not None:
                end = end2
            if rep is not None:
                self.pkahelper.rep = rep
            xml2 = xml


        options = QFileDialog.Options()
        work_dir = os.getcwd()+"\\files"
        file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Packet Tracer File (*."+end+");;All Files (*)", options=options)
        
        if file_name:
            string:bytes = etree.tostring(xml2, method="c14n")
            self.pkahelper.encrypt(string.decode("utf-8"),end, file_name)
            msg = QMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Finished")
            msg.setIcon(QMessageBox.Information)
            msg.addButton(QMessageBox.Ok)
            msg.exec()
            try:
                file_path="files/decrypted.xml"
                os.system(f'start {file_name}')
            except:
                pass

            
            

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernUI()
    window.show()
    sys.exit(app.exec_())