import pyglet
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as OpenGLWidget
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from pyglet.gl import *
from PyQt5.QtCore import Qt


class PygletWidget(OpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        width, height = 640, 480
        self.setMinimumSize(width, height)

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


    def _pyglet_update(self):
        # Tick the pyglet clock, so scheduled events can work.
        pyglet.clock.tick()  
        
        # Force widget to update, otherwise paintGL will not be called.
        self.update()  # self.updateGL() for pyqt5

    def paintGL(self):
        """Pyglet equivalent of on_draw event for window"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        self.batch.draw()


    def initializeGL(self):
        """Call anything that needs a context to be created."""
        self.batch = pyglet.graphics.Batch()
        size = self.size()
        w, h = size.width(), size.height()
        
        self.projection = pyglet.window.Projection2D()
        self.projection.set(w, h, w, h)

    def mouseMoveEvent(self, event):
        # Handle mouse movement and update camera position
        if event.buttons() == Qt.LeftButton:
            current_pos = event.pos()
            if self.last_mouse_pos is None:
                self.last_mouse_pos = current_pos
            dx = (current_pos.x() - self.last_mouse_pos.x())
            dy =- (current_pos.y() - self.last_mouse_pos.y())

            # new_camera_x = self.camera_x - dx
            # new_camera_y = self.camera_y - dy

            # # Check if new_camera_x is within limits
            # if self.camera_x_min <= new_camera_x <= self.camera_x_max:
            #     self.camera_x = new_camera_x
            # else:
            #     dx = 0

            # # Check if new_camera_y is within limits
            # if self.camera_y_min <= new_camera_y <= self.camera_y_max:
            #     self.camera_y = new_camera_y
            # else:
            #     dx = 0

            glTranslatef(dx, dy, 0)
            self.update()
            self.last_mouse_pos = current_pos

            
    def mouseReleaseEvent(self, event):
        # Reset last mouse position when the mouse button is released
        self.last_mouse_pos = None

    def wheelEvent(self, event):
        # Handle mouse wheel event for zooming
        angleDeltaY = event.angleDelta().y()
        zoom_speed = 0.01  # Adjust zoom speed as needed
        print("Angle Delta")
        print(angleDeltaY)
        # Update the camera scale while respecting the limits
        new_scale = self.camera_scale - angleDeltaY * zoom_speed
        if 0.1 <= new_scale <= 2.0:  # Adjust the zoom limits as needed
            self.camera_scale = new_scale
        print("Camera scale")
        print(self.camera_scale)
        print("Value")
        print(angleDeltaY*zoom_speed)
        glScalef(angleDeltaY*zoom_speed, angleDeltaY*zoom_speed, 1.0)
        self.update()