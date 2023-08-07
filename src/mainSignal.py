import sys
import pyglet
import random

from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as OpenGLWidget
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt

from pygletWidget import PygletWidget
from ui_mainGUI import Ui_MainWindow
from tileMapper import TileMapper
from extra import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Signalling Simulator")

        self.opengl = self.ui.openGLWidget
        self.tileMap = None

        self.ui.actionOpen_Map.triggered.connect(self.openMap)

        self.ui.actionRed.triggered.connect(lambda: self.setSignal("Red"))
        self.ui.actionyellow.triggered.connect(lambda: self.setSignal("DYellow"))
        self.ui.actiondYellow.triggered.connect(lambda: self.setSignal("Yellow"))
        self.ui.actionGreen.triggered.connect(lambda: self.setSignal("Green"))

        self.ui.actionToggle_Track.triggered.connect(self.togglePoint)

        self.ui.actionZoom_In.triggered.connect(lambda: self.opengl.zoomScreen(1/1.2,self.opengl.width/2,self.opengl.height/2))
        self.ui.actionZoom_Out.triggered.connect(lambda: self.opengl.zoomScreen(1.2,self.opengl.width/2,self.opengl.height/2))
        self.ui.actionActual_Size.triggered.connect(self.zoomToActualSize)


        self.setMouseTracking(True)
        self.installEventFilter(self)

        
    def openMap(self):
        self.tileMap = TileMapper(self.opengl,self.opengl.shapes)
        #try:
        self.tileMap.openFile(QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)"))
        # except: 
        #     print("File Failed to open")
        #     popup = PopupWindow("File failed to open", "Error").exec_()
        self.opengl.mousePressSignal.connect(self.tileMap.canvasMousePressEvent)
        self.zoomToActualSize()

    def setSignal(self, type):
        if self.tileMap!=None:
            self.tileMap.setSignal(type)

    def togglePoint(self):
        print("Toggling")
        if self.tileMap!=None:
            self.tileMap.togglePoint()

    def zoomToActualSize(self):

        zoomHeightOld = self.opengl.zoomed_height
        prop = self.opengl.zoomed_width / self.opengl.zoomed_height

        if self.tileMap.width>self.tileMap.height:
            self.opengl.zoomed_width = self.tileMap.width*50
            self.opengl.zoomed_height = self.opengl.zoomed_width /prop
        else:
            self.opengl.zoomed_height = self.tileMap.height*50
            self.opengl.zoomed_width = self.opengl.zoomed_height * prop

        self.opengl.left = 0
        self.opengl.bottom = 0
        self.opengl.right = self.opengl.zoomed_width
        self.opengl.top = self.opengl.zoomed_height

        self.opengl.zoom_level = self.opengl.zoom_level * (self.opengl.zoomed_height/zoomHeightOld)



if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
