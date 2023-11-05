

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QListWidget, QSlider, QPushButton
import os
import importlib
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
from PkaHelper import PkaHelper
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea
import copy

bs = '''
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
        '''
filename = None
xml = None
pka = PkaHelper()

class ManipulationDialog(QDialog):
    def __init__(self):
        super().__init__()
        global name
        self.setWindowTitle(name)
        self.setFixedSize(500,200)
        layout = QVBoxLayout()

        filechooseWiget = QWidget()
        hl = QHBoxLayout()
        lable = QLabel("kein file selected")
        button = QPushButton("choose")
        button.setFixedSize(100,60)
        button.setStyleSheet(bs)
        button.clicked.connect(self.openFileDialog)
        hl.addWidget(lable)
        self.lable33 = lable
        hl.addWidget(button)
        filechooseWiget.setLayout(hl)
        layout.addWidget(filechooseWiget)

        layout.addWidget(QLabel("Takes the packet tracer file and inserts the devices and so one into it. Useful for files, where \ncopying is diabled."))
        layout.addWidget(QLabel(""))
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(bs)
        ok_button.clicked.connect(self.accept)  
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def openFileDialog(self,a):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Packet Tracer Files (*.pka *.pkt)", options=options)
       
        if file_name:
            global xml 
            global filename
            global pka
            xml = pka.decrypt(file_name,file_name.split(".")[-1])
            filename = file_name
            self.lable33.setText(file_name.split("/")[-1])


name = "Copy Devices into File"
def manipulate(xmld):
    global xml
    global filename
    global pka

    destinations = xml.xpath("//PACKETTRACER5")
    source = xmld.xpath("//PACKETTRACER5"   )[0]

    for destination in destinations:
        xml.replace(destination,copy.deepcopy(source))

    return xml,filename.split(".")[-1], pka.rep

def settings(xml):
    ManipulationDialog().exec()