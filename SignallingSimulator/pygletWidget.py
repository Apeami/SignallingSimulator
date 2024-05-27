import pyglet
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as OpenGLWidget
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from pyglet.gl import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
import math
from pyglet.math import Mat4
from pyglet import shapes


# Zooming constants
ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR

class PygletWidget(OpenGLWidget):
    mousePressSignal = pyqtSignal(int, int,int,int,int,int,int,int)


    def __init__(self, parent):
        super().__init__(parent)
        width, height = 1441, 521
        #self.setMinimumSize(width, height)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._pyglet_update)
        self.timer.setInterval(0)
        self.timer.start()


        self.last_mouse_pos = None
        self.dy = 0
        self.dx = 0
        self.camera_x, self.camera_y = 0, 0

        self.camera_x_min = -40  # Set the minimum X coordinate limit
        self.camera_x_max = 40   # Set the maximum X coordinate limit
        self.camera_y_min = -40  # Set the minimum Y coordinate limit
        self.camera_y_max = 40   # Set the maximum Y coordinate limit

        self.camera_scale = 1

        self.shapes = []
        self.batchList = {}



    def _pyglet_update(self):
        # Tick the pyglet clock, so scheduled events can work.
        pyglet.clock.tick()  
        
        # Force widget to update, otherwise paintGL will not be called.
        self.update()  # self.updateGL() for pyqt5

    def paintGL(self):
        """Pyglet equivalent of on_draw event for window"""
        
        # Initialize Projection matrix
        # glMatrixMode( GL_PROJECTION )
        # glLoadIdentity()

        # # Initialize Modelview matrix
        # glMatrixMode( GL_MODELVIEW )
        # glLoadIdentity()
        # # Save the default modelview matrix
        # glPushMatrix()

        glClearColor(0.0, 0.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        print(current_context)
        print(self.context())

        # pyglet.window.projection = Mat4.orthogonal_projection(
        #     self.left, self.right, self.bottom, self.top, 1, -1
        # )
        pyglet.window.projection = Mat4.orthogonal_projection(
            -5, 5, -5, 5, 1, -1
        )
        # Set orthographic projection matrix
        #glOrtho( self.left, self.right, self.bottom, self.top, 1, -1 )

        # Draw quad 
        # glBegin( GL_QUADS )
        # glColor3ub( 0xFF, 0, 0 )
        # glVertex2i( 10, 10 )

        # glColor3ub( 0xFF, 0xFF, 0 )
        # glVertex2i( 110, 10 )

        # glColor3ub( 0, 0xFF, 0 )
        # glVertex2i( 110, 110 )

        # glColor3ub( 0, 0, 0xFF )
        # glVertex2i( 10, 110 )
        # glEnd()

        shapes.Rectangle(200, 200, 200, 200, color=(55, 55, 255)).draw()

        # self.batch.draw()

        # for batch in self.batchList:
        #     self.batchList[batch].draw()

        # Remove default modelview matrix
        #glPopMatrix()     
        
        
    def resizeGL(self, width, height):
        print("Resized to:", width, "x", height)
        prevWidth  = self.width
        prevHeight = self.height

        prevZoomWidth = self.right - self.left
        prevZoomHeight = self.bottom - self.top

        CZoomWidth = (width * prevZoomWidth) // prevWidth
        CZoomHeight = (height * prevZoomHeight) // prevHeight

        self.right = self.left + CZoomWidth
        self.top = self.bottom + CZoomHeight

        self.zoom_level = 1
        self.zoomed_width  = width
        self.zoomed_height = height

        self.width = width
        self.height = height

        self.zoomScreen(1.2,0,0)
        self.zoomScreen(0.833,0,0)
        #self.projection.set(self.width, self.height, self.width, self.height)

    def initializeGL(self):
        """Call anything that needs a context to be created."""
        self.batch = pyglet.graphics.Batch()
        size = self.size()
        self.width, self.height = size.width(), size.height()
        
        # self.projection = pyglet.window.Projection2D()
        # self.projection.set(self.width, self.height, self.width, self.height)
        # pyglet.window.projection = Mat4.orthogonal_projection(
        #     0, self.width, 0, self.height, -255, 255
        # )

        self.left   = 0
        self.right  = self.width
        self.bottom = 0
        self.top    = self.height
        self.zoom_level = 1
        self.zoomed_width  = self.width
        self.zoomed_height = self.height

    def mouseMoveEvent(self, event):
        # Handle mouse movement and update camera position
        if event.buttons() == Qt.LeftButton:
            current_pos = event.pos()
            if self.last_mouse_pos is None:
                self.last_mouse_pos = current_pos
            dx = (current_pos.x() - self.last_mouse_pos.x())
            dy =- (current_pos.y() - self.last_mouse_pos.y())

            self.left   -= dx*self.zoom_level
            self.right  -= dx*self.zoom_level
            self.bottom -= dy*self.zoom_level
            self.top    -= dy*self.zoom_level

            self.last_mouse_pos = current_pos

            
    def mouseReleaseEvent(self, event):
        # Reset last mouse position when the mouse button is released
        self.last_mouse_pos = None

    def wheelEvent(self,event):
        f = ZOOM_OUT_FACTOR if event.angleDelta().y() > 0 else ZOOM_IN_FACTOR if event.angleDelta().y() < 0 else 1
        x = event.pos().x()
        y = event.pos().y()
        self.zoomScreen(f,x,y)

    def zoomScreen(self, f,x,y):
        print(f)
        # If zoom_level is in the proper range
        if .2 < self.zoom_level*f < 5:
            self.zoom_level *= f



            mouse_x = x/self.width
            mouse_y = y/self.height

            mouse_x_in_world = self.left   + mouse_x*self.zoomed_width
            mouse_y_in_world = self.bottom + mouse_y*self.zoomed_height

            self.zoomed_width  *= f
            self.zoomed_height *= f

            self.left   = mouse_x_in_world - mouse_x*self.zoomed_width
            self.right  = mouse_x_in_world + (1 - mouse_x)*self.zoomed_width
            self.bottom = mouse_y_in_world - mouse_y*self.zoomed_height
            self.top    = mouse_y_in_world + (1 - mouse_y)*self.zoomed_height

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            self.mousePressSignal.emit(x, y,self.left,self.right,self.top,self.bottom,self.width,self.height)  # Emit the signal with x and y coordinates

    def zoomToActualSize(self,tilemap):

        zoomHeightOld = self.zoomed_height
        prop = self.zoomed_width / self.zoomed_height

        if tilemap.width>tilemap.height:
            self.zoomed_width = tilemap.width*50
            self.zoomed_height = self.zoomed_width /prop
        else:
            self.zoomed_height = tilemap.height*50
            self.zoomed_width = self.zoomed_height * prop

        self.left = 0
        self.bottom = 0
        self.right = self.zoomed_width
        self.top = self.zoomed_height

        self.zoom_level = self.zoom_level * (self.zoomed_height/zoomHeightOld)

    def createNewBatch(self, name):
        batch = pyglet.graphics.Batch()

        self.batchList[name] = batch

        return batch

    def removeBatch(self, name):
        if name in self.batchList:
            del self.batchList[name]

