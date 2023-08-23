import sys
import pyglet
import random
import time


from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as OpenGLWidget
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
import logging

from pygletWidget import PygletWidget
from ui_mainGUI import Ui_MainWindow
from tileMapper import TileMapper
from extra import *

from train import Train
from clock import Clock
from timetable import Timetable
from eventBox import EventBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setui the ui and window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signalling Simulator")

        #Get the opengl widget
        self.opengl = self.ui.openGLWidget

        #These are the maps to be loaded
        self.tileMap = None
        self.timetable = None

        #Bind the actions
        self.ui.actionOpen_Map.triggered.connect(self.openMap)
        self.ui.actionOpen_Timetable.triggered.connect(self.openTimetable)
        self.ui.actionNew_Simulation.triggered.connect(self.newMap)

        self.ui.actionRed.triggered.connect(lambda: self.setSignal("Red"))
        self.ui.actionyellow.triggered.connect(lambda: self.setSignal("DYellow"))
        self.ui.actiondYellow.triggered.connect(lambda: self.setSignal("Yellow"))
        self.ui.actionGreen.triggered.connect(lambda: self.setSignal("Green"))

        self.ui.actionToggle_Track.triggered.connect(self.togglePoint)

        self.ui.actionZoom_In.triggered.connect(lambda: self.opengl.zoomScreen(1/1.2,self.opengl.width/2,self.opengl.height/2))
        self.ui.actionZoom_Out.triggered.connect(lambda: self.opengl.zoomScreen(1.2,self.opengl.width/2,self.opengl.height/2))
        self.ui.actionActual_Size.triggered.connect(lambda: self.opengl.zoomToActualSize(self.tileMap))

        #Enable events
        self.setMouseTracking(True)
        self.installEventFilter(self)

        #Setup Clock
        Clock(self.ui)

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
        
        self.tileMap = TileMapper(self.opengl,self.opengl.shapes)
        #try:
        self.tileMap.openFile(QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)"))
        # except: 
        #     print("File Failed to open")
        #     popup = PopupWindow("File failed to open", "Error").exec_()
        self.opengl.mousePressSignal.connect(self.tileMap.canvasMousePressEvent)
        self.opengl.zoomToActualSize(self.tileMap)

    def openTimetable(self):
        self.timetable = Timetable(self.opengl,self.opengl.shapes,self.ui)
        self.timetable.openFile(QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)"))
        self.opengl.mousePressSignal.connect(self.timetable.canvasMousePressEvent)

    def newMap(self):
        #AKA reset everything
        self.timetable = None
        self.tileMap = None
        self.opengl.shapes = []

    def setSignal(self, type):
        if self.tileMap!=None:
            self.tileMap.setSignal(type)

    def togglePoint(self):
        print("Toggling")
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
    
