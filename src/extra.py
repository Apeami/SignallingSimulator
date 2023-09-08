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
    _image_cache = {}  # Global cache to store images and their color settings

    def __init__(self, image_path):

        self.image_path = image_path
        self.replace_color = (0, 0, 255)  # Default replacement color is blue
        self.origin_color = (255,255,255)

    def set_replacement_color(self, color):
        self.replace_color = color

    def set_origin_color(self,color):
        self.origin_color = color

    def render(self):
        # Create a unique key based on image_path and color settings
        cache_key = (self.image_path, self.origin_color, self.replace_color)

        if cache_key not in self._image_cache:
            # If the image is not in the cache, load it and process it
            original_image = pyglet.image.load(self.image_path)
            image_data = original_image.get_image_data()
            pixel_data = image_data.get_data("RGBA", original_image.width * 4)
            pixels = [(pixel_data[i], pixel_data[i + 1], pixel_data[i + 2], pixel_data[i + 3])
                      for i in range(0, len(pixel_data), 4)]

            modified_pixel_data = bytearray()
            for pixel in pixels:
                if pixel[:3] == self.origin_color:
                    modified_pixel_data.extend(
                        bytes([self.replace_color[0], self.replace_color[1], self.replace_color[2], pixel[3]]))
                else:
                    modified_pixel_data.extend(bytes(pixel))

            modified_image = pyglet.image.ImageData(original_image.width, original_image.height, 'RGBA',
                                                    bytes(modified_pixel_data))

            # Cache the modified image and its color settings for future use
            self._image_cache[cache_key] = modified_image
        else:
            # If the image is in the cache, use the cached version
            modified_image = self._image_cache[cache_key]

        return modified_image