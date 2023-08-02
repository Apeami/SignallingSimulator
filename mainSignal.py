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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.setWindowTitle("Pyglet and QT Example")
        #self.shapes = []

        width, height = 640, 480
        self.opengl = self.ui.openGLWidget

        self.sprite_button = self.ui.CreateRect
        self.sprite_button.clicked.connect(self.create_sprite_click)

        self.clear_sprite_button = self.ui.pushButton
        self.clear_sprite_button.clicked.connect(self.clear_sprite_click)
        
        
        
        self.ui.actionOpen_Map.triggered.connect(self.openMap)


        
        #self.ui.actionOpen_Map.triggered.connect(self.start)

        self.setMouseTracking(True)
        self.installEventFilter(self)

        
    def openMap(self):
        self.tileMap = TileMapper(self.opengl,self.opengl.shapes)
        self.tileMap.openFile(QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)"))
        self.opengl.mousePressSignal.connect(self.tileMap.canvasMousePressEvent)


    def create_sprite_click(self):
        gl_width, gl_height = self.opengl.size().width(), self.opengl.size().height()

        # Load the image and create a sprite
        image_path = "assets/platform.png"
        image = pyglet.image.load(image_path)
        sprite = pyglet.sprite.Sprite(image, batch=self.opengl.batch)

        # Set the initial position for the sprite
        x = random.randint(0, gl_width - 50)
        y = random.randint(0, gl_height - 50)
        print(x,y)
        sprite.update(x, y)

        # Add the sprite to the list of shapes
        self.opengl.shapes.append(sprite)
        
    def clear_sprite_click(self):
        for shape in self.opengl.shapes:
            shape.delete()
            
        self.opengl.shapes.clear()



if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
