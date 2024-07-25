#!/usr/bin/python3
import sys
import random
import time
import logging

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox,QWidget
from PyQt5.QtCore import Qt, QProcess

from ui_mainGUI import Ui_MainWindow
from tileMapper import TileMapper

from extra import *
from train import Train
from clock import Clock
from timetable import Timetable
import helpwindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setui the ui and window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signalling Simulator")
        self.show()

        #Initialize clock to null
        self.clock = None

        #Get the map widget
        self.map_draw = self.ui.MapWidget

        #These are the maps to be loaded
        self.tileMap = None
        self.timetable = None

        #Initial Window
        self.welcome = helpwindow.WelcomeWindow()
        self.welcome.show()

        #Bind the actions
        self.ui.actionOpen_Map.triggered.connect(self.openMap)
        self.ui.actionOpen_Timetable.triggered.connect(self.openTimetable)
        self.ui.actionNew_Simulation.triggered.connect(self.newMap)

        self.ui.actionRed.triggered.connect(lambda: self.setSignal("Red"))
        self.ui.actionyellow.triggered.connect(lambda: self.setSignal("Yellow"))
        self.ui.actiondYellow.triggered.connect(lambda: self.setSignal("DYellow"))
        self.ui.actionGreen.triggered.connect(lambda: self.setSignal("Green"))

        self.ui.actionToggle_Track.triggered.connect(self.togglePoint)

        self.ui.actionZoom_In.triggered.connect(lambda: self.map_draw.zoomScreen(1/1.2))
        self.ui.actionZoom_Out.triggered.connect(lambda: self.map_draw.zoomScreen(1.2))
        self.ui.actionActual_Size.triggered.connect(lambda: self.map_draw.zoomToActualSize(self.tileMap))

        self.ui.actionHelp.triggered.connect(lambda: self.welcome.showHelp(mainwindow = self))



        #Enable events
        self.setMouseTracking(True)
        self.installEventFilter(self)

        #Setup EventBox
        self.textBox = self.ui.LogTextBox
        self.textBox.setReadOnly(True)

        self.logger = logging.getLogger("my_logger")
        self.logger.setLevel(logging.INFO)

        # Create a handler to direct log messages to the QTextEdit widget
        handler = QtHandler(self.textBox)
        self.logger.addHandler(handler)
        self.logger.info("Started the simulator")

    
    def openMap(self):
        
        if self.tileMap!=None:
            confirm_box = QMessageBox(self)
            confirm_box.setIcon(QMessageBox.Question)
            confirm_box.setWindowTitle('Confirmation')
            confirm_box.setText('You have a map open already, are you sure you want to open another one?')
            confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_box.setDefaultButton(QMessageBox.No)

            button_clicked = confirm_box.exec_()

            if button_clicked == QMessageBox.No:
                return

        self.map_draw.del_all_train()
        self.map_draw.del_all_tile()
        if self.timetable!=None:
            self.timetable.delete()
        if self.tileMap!=None:
            self.tileMap.delete()
        self.timetable = None
        del self.tileMap
        self.tileMap = TileMapper(self.map_draw)

        if self.clock!=None:
            self.clock.reset()


        fileName = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")

        if fileName!=('', ''): #User cancelled the file selection process
            # try:
            self.tileMap.openFile(fileName)
            # except:
                # print("File Failed to open")
                # popup = WarningBox("File failed to open", "Error").exec_()
                # self.connectMapFunction()
                # self.tileMap=None
                # return
        else:
            print("File Search cancelled")
            self.connectMapFunction()
            self.tileMap=None
            return

        self.connectMapFunction()

        #Alert the user
        self.logger.info("Succesfully opened the map")

    def connectMapFunction(self):
        #Connect the actions related routing
        self.ui.actionAuto_Track.triggered.connect(self.tileMap.manageAutoTrack)
        self.ui.actionRoute_Train.triggered.connect(self.tileMap.manageTrainRoute)
        self.ui.actionDeleteRouting.triggered.connect(self.tileMap.manageDeleteRouting)

        #Connect the mouse and zoom to the map
        self.map_draw.mousePressSignal.connect(self.tileMap.canvasMousePressEvent)
        self.map_draw.zoomToActualSize(self.tileMap)

    def openTimetable(self):
        if self.tileMap!=None:
            if self.timetable!=None:
                confirm_box = QMessageBox(self)
                confirm_box.setIcon(QMessageBox.Question)
                confirm_box.setWindowTitle('Confirmation')
                confirm_box.setText('You have a timetable open already, are you sure you want to open another one?')
                confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm_box.setDefaultButton(QMessageBox.No)

                button_clicked = confirm_box.exec_()

                if button_clicked == QMessageBox.No:
                    return

            self.timetable = Timetable(self.map_draw,self.ui, self.tileMap)
            fileName = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
            if fileName!=('',''):
                self.timetable.openFile(fileName)
            else:
                print("File Search Cancelled")
                self.timetable=None
                return


            self.map_draw.mousePressSignal.connect(self.timetable.canvasMousePressEvent)
            self.ui.ZoomToTrainButton.clicked.connect(self.timetable.zoomtoselectedtrain)

            #Here is when the timetable is loaded, the simulation can begin
            #Setup Clock
            self.clock = Clock(self.ui,self.timetable.updateClock,self.timetable.startTime)

            print("create handleer")
            #Create A handler for the clicks of Train List and Train Information
            self.ui.TrainList.cellDoubleClicked.connect(self.trainlistclicked)
            self.ui.TrainTimetable.cellDoubleClicked.connect(self.traintimetableclicked)


            #Alert user
            self.logger.info("Succesfully opened the timetable")

        else:
            print("No Tilemap imported")
            popup = WarningBox("No map imported yet. Cannot import timetable", "Info").exec_()

    def trainlistclicked(self, row, column):
        item = self.ui.TrainList.item(row, 0)  # Get the item in the first column of the clicked row
        if item:
            self.timetable.zoomtotrain(item.text())

    def traintimetableclicked(self,row,column):
        print("Clicked")
        print(self.timetable.selectedTrainIndex)
        if self.timetable.selectedTrainIndex!=None:
            print("HEre")
            train = self.timetable.trainList[self.timetable.selectedTrainIndex]
            loc = train.sorted_schedule[row]['Location']
            print(train)
            print(loc)
            self.tileMap.zoomtopoint(loc)

    def newMap(self):
        if self.tileMap!=None or self.timetable!=None:
            confirm_box = QMessageBox(self)
            confirm_box.setIcon(QMessageBox.Question)
            confirm_box.setWindowTitle('Confirmation')
            confirm_box.setText('You have a timetable open already, are you sure you want to start a new session?')
            confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_box.setDefaultButton(QMessageBox.No)

            button_clicked = confirm_box.exec_()

            if button_clicked == QMessageBox.Yes:
                if self.timetable!=None:
                    self.timetable.delete()
                if self.tileMap!=None:
                    self.tileMap.delete()
                self.timetable = None
                self.tileMap = None
                self.opengl.shapes = []

                for child in self.ui.centralwidget.children():
                    if isinstance(child, QWidget):
                        child.deleteLater()

                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
        

    def setSignal(self, type):
        if self.tileMap!=None:
            self.tileMap.setSignal(type)

    def togglePoint(self):
        if self.tileMap!=None:
            self.tileMap.togglePoint()

class QtHandler(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        log_message = self.format(record)
        self.text_edit.append(log_message)


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
