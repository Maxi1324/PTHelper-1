

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
from ManipulationDialog import ManipulationDialog
from PkaHelper import PkaHelper
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea
import copy
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateTimeEdit
from PyQt5.QtCore import QDateTime, pyqtSlot


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

        datetimeedit = QDateTimeEdit(self)
        datetimeedit.setDateTime(QDateTime.currentDateTime())  # Standarddatum und -uhrzeit setzen
        datetimeedit.setCalendarPopup(True) 
        hl.addWidget(datetimeedit)
        datetimeedit.dateTimeChanged.connect(self.change)


        filechooseWiget.setLayout(hl)
        layout.addWidget(filechooseWiget)

        layout.addWidget(QLabel("Set the start time of the PTFile"))
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(bs)
        ok_button.clicked.connect(self.accept)  
        layout.addWidget(ok_button)

        self.setLayout(layout)

    @pyqtSlot(QDateTime)
    def change(self, vali):
        global val
        val = vali.toString("yyyy-MM-dd hh:mm:ss")
         

                
                

name = "Change Start Time"
def manipulate(xml):
    global val
    timestamp = xml.xpath("//START_TIMESTAMP")
    for t in timestamp:
        t.text = val

    return (xml,None,None)
def settings(xml):
    ManipulationDialog().exec()