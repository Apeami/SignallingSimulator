from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
import pyglet
from pyglet.image import SolidColorImagePattern


class WarningBox(QDialog):
    def __init__(self,message,title):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(300, 150)  # Set the window size

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add content to the popup
        label = QLabel(message)
        layout.addWidget(label)

        # Add a close button
        close_button = QPushButton("OK")
        close_button.clicked.connect(self.close)  # Close the popup when the button is clicked
        layout.addWidget(close_button)

class ConfirmationBox(QDialog):
    def __init__(self,message,title,callFunction):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(300, 150)  # Set the window size

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add content to the popup
        label = QLabel(message)
        layout.addWidget(label)

        # Add a close button
        cancel = QPushButton("Close")
        close_button.clicked.connect(self.close)  # Close the popup when the button is clicked
        layout.addWidget(close_button)

class ReplacableImage:
    def __init__(self, image_path):
        self.original_image = pyglet.image.load(image_path)
        self.replace_color = (0, 0, 255)  # Default replacement color is blue
        self.origin_color = (255,255,255)

    def set_replacement_color(self, color):
        self.replace_color = color

    def set_origin_color(self,color):
        self.origin_color = color

    def render(self):
        if self.replace_color is None:
            return self.original_image

        image_data = self.original_image.get_image_data()
        pixel_data = image_data.get_data("RGBA", self.original_image.width * 4)
        pixels = [(pixel_data[i], pixel_data[i+1], pixel_data[i+2], pixel_data[i+3]) for i in range(0, len(pixel_data), 4)]

        modified_pixel_data = bytearray()
        for pixel in pixels:
            if pixel[:3] == self.origin_color:  # Replace white pixels
                modified_pixel_data.extend(bytes([self.replace_color[0], self.replace_color[1], self.replace_color[2], pixel[3]]))
            else:
                modified_pixel_data.extend(bytes(pixel))

        modified_image = pyglet.image.ImageData(self.original_image.width, self.original_image.height, 'RGBA', bytes(modified_pixel_data))

        return modified_image