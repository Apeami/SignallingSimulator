#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QDialog, QScrollArea, QVBoxLayout, QTextEdit

import helpwindow
from mapPlayer import MapPlayer
from mapEditor import MapEditor

class MainSignal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set up the window
        self.setWindowTitle('Welcome to Signalling Simulator')
        self.setGeometry(100, 100, 300, 200)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Welcome label
        welcome_label = QLabel('Welcome to the Railway Signalling Simulator!', self)
        layout.addWidget(welcome_label)
        
        # Introduction label
        welcome_label = QLabel('''

To get started, follow these steps:\n

    1) Open a Map: Navigate to File > Open Map to select and load a map. \n
    2)Open a Timetable: Every map has one or more associated timetables. To open a timetable, go to File > Open Timetable.\n
    3) Start the Simulation: Once you have opened the timetable, press the start button to begin the simulation.\n

Controls:\n

    1) Signals and Points: Use the toolbar buttons to control the signals and points on the map. \n
     2)Train Information: Click on the trains to view details about their intended routes. \n

For additional assistance, click the Help button below or access help via File > Help.

Enjoy managing your railway network!''', self)
        layout.addWidget(welcome_label)
        
        play_btn = QPushButton('Simulation Player', self)
        play_btn.clicked.connect(lambda: self.playButton())
        layout.addWidget(play_btn)

        edit_btn = QPushButton('Simulation Editor', self)
        edit_btn.clicked.connect(lambda: self.editButton())
        layout.addWidget(edit_btn)

        help_btn = QPushButton('Help', self)
        help_btn.clicked.connect(lambda: helpwindow.showIntroHelp(self))
        layout.addWidget(help_btn)
        
        # Set layout
        self.setLayout(layout)

        #Set subwindow variable
        self.playWindow = None
        self.editWindow = None
    
    def playButton(self):
        print("User chose play")
        self.close()

        if self.editWindow!=None:
            self.editWindow.close()

        self.playWindow = MapPlayer(self)
        self.playWindow.show()



    def editButton(self):
        print("User chose edit")
        self.close()

        if self.playWindow!=None:
            self.playWindow.close()

        self.editWindow = MapEditor(self)
        self.editWindow.show()


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = MainSignal()
    window.show()
    sys.exit(app.exec_())
    
