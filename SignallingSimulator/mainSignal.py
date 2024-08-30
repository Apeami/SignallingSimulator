#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QDialog, QScrollArea, QVBoxLayout, QTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets

import helpwindow
from mapPlayer import MapPlayer
from mapEditor import MapEditor
import ui_welcomeScreen
import json
import os

class MainSignal(ui_welcomeScreen.Ui_Form):
    def __init__(self):
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)

        self.mainWidget.setWindowTitle('Welcome to Signalling Simulator')

        self.playButton.clicked.connect(lambda: self.playButtonCallback())
        self.editButton.clicked.connect(lambda: self.editButtonCallback())
        self.helpButton.clicked.connect(lambda: helpwindow.showIntroHelp(self.mainWidget))

        #Set subwindow variable
        self.playWindow = None
        self.editWindow = None

        #Gather example files
        for entry in os.listdir(base_dir):
            entry_path = os.path.join(base_dir, entry)
            if os.path.isdir(entry_path):
                json_file_path = os.path.join(entry_path, f"{entry}.json")
                if os.path.isfile(json_file_path):
                    try:
                        with open(json_file_path, 'r') as json_file:
                            data = json.load(json_file)
                            print(data)        
                            self.addExampleField(data["name"], data["description"], data["map"], data["timetable"][0])
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {json_file_path}")

        #Add final spacer item
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ScrollAreaLayout.addItem(spacerItem)

        #Show final window
        self.mainWidget.show()

    def addExampleField(self, name, description, mapName, timetableName):
        playButton = QtWidgets.QPushButton()
        playButton.setText("Play Map")
        playButton.setProperty("map", mapName)
        playButton.setProperty("timetable", timetableName)
        playButton.clicked.connect(self.openMapButtonClicked)
        # self.playPushButtons.append(playButton)
        
        labelName = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        labelName.setFont(font)
        labelName.setText(name)

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.addWidget(labelName)
        verticalLayout.addWidget(playButton)


        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        labelDesc = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        labelDesc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        labelDesc.setWordWrap(True)
        labelDesc.setText(description)

        templateMapInfo = QtWidgets.QHBoxLayout()
        templateMapInfo.addLayout(verticalLayout)
        templateMapInfo.addWidget(line)
        templateMapInfo.addWidget(labelDesc)

        self.ScrollAreaLayout.addLayout(templateMapInfo)

    def openMapButtonClicked(self):
        button = self.mainWidget.sender()
        mapName = button.property("map")
        timetableName = button.property("timetable")

        print(mapName)
        print(timetableName)

        self.playButtonCallback()
        self.playWindow.openMap(fileName=mapName)
        self.playWindow.openTimetable(fileName=timetableName)

    def playButtonCallback(self):
        print("User chose play")
        self.mainWidget.close()

        if self.editWindow!=None:
            self.editWindow.close()

        self.playWindow = MapPlayer(self)
        self.playWindow.show()

    def editButtonCallback(self):
        print("User chose edit")
        self.mainWidget.close()

        if self.playWindow!=None:
            self.playWindow.close()

        self.editWindow = MapEditor(self)
        self.editWindow.show()

    def load_json_from_file(self, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data


if __name__ == '__main__':    
    base_dir = "../Examples"
    app = QApplication(sys.argv)
    window = MainSignal()
    sys.exit(app.exec_())
    
