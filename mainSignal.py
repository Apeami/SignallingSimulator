import sys
import pyglet
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as OpenGLWidget
#from PyQt6 import QtGui
#from PyQt6 import QtCore, QtWidgets
#from PyQt6.QtOpenGLWidgets import QOpenGLWidget as OpenGLWidget
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import random
from PyQt5.QtWidgets import QApplication, QMainWindow

from pygletWidget import PygletWidget
from ui_mainGUI import Ui_MainWindow


"""An example showing how to use pyglet in QT, utilizing the OGLWidget.

   Since this relies on the QT Window, any events called on Pyglet Window
   will NOT be called.
    
   This includes mouse, keyboard, tablet, and anything else relating to the Window
   itself. These must be handled by QT itself.
   
   This just allows user to create and use pyglet related things such as sprites, shapes,
   batches, clock scheduling, sound, etc.           
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.setWindowTitle("Pyglet and QT Example")
        self.shapes = []

        width, height = 640, 480
        self.opengl = self.ui.openGLWidget

        self.sprite_button = self.ui.CreateRect
        self.sprite_button.clicked.connect(self.create_sprite_click)

        self.clear_sprite_button = self.ui.pushButton
        self.clear_sprite_button.clicked.connect(self.clear_sprite_click)
        
        # mainLayout = QtWidgets.QVBoxLayout()
        # mainLayout.addWidget(self.opengl)
        # mainLayout.addWidget(self.sprite_button)
        # mainLayout.addWidget(self.clear_sprite_button)
        # self.setLayout(mainLayout)

        self.setMouseTracking(True)
        self.installEventFilter(self)

    def create_sprite_click(self):
        gl_width, gl_height = self.opengl.size().width(), self.opengl.size().height()
        print(gl_width)
        print(gl_height)


        width = random.randint(50, 100)
        height = random.randint(50, 100)
        
        x = random.randint(0, gl_width-width)
        y = random.randint(0, gl_height-height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        shape = pyglet.shapes.Rectangle(x, y, width, height, color=color, batch=self.opengl.batch)
        shape.opacity = random.randint(100, 255)
        self.shapes.append(shape)
        
    def clear_sprite_click(self):
        for shape in self.shapes:
            shape.delete()
            
        self.shapes.clear()


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
