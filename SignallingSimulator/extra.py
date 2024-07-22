from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton


from PyQt5.QtCore import Qt, QByteArray, QBuffer
from PyQt5.QtGui import QImage, QPixmap, QTransform

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
        self.replace_color = (0, 255, 255,255)  # Default replacement color is blue
        self.origin_color = (255,255,255,255)
        self.width=0
        self.height=0
        self.flip = False
        self.point =0

    def set_replacement_color(self, color):
        self.replace_color = color

    def set_origin_color(self,color):
        self.origin_color = color

    def transform_modified_image(self, image):

        if self.flip:
            image = image.transformed(QTransform().scale(1, -1))

        if self.point!=0:
            image = image.transformed(QTransform().rotate(self.point))



        self.width = image.width()
        self.height = image.height()

        return image

    def render(self):
        # Create a unique key based on image_path and color settings
        cache_key = (self.image_path, self.origin_color, self.replace_color)

        if cache_key not in self._image_cache:
            # If the image is not in the cache, load it and process it
            # original_image = pyglet.image.load(self.image_path)
            # image_data = original_image.get_image_data()


            image = QImage(self.image_path)



                # Ensure image format is RGBA32 to access raw bytes easily
            image = image.convertToFormat(QImage.Format_RGBA8888)

            # Access raw bytes
            width = image.width()
            height = image.height()
            bytes_per_line = image.bytesPerLine()
            ptr = image.bits()

            if ptr == None:
                raise Exception("No asset file found") 

            ptr.setsize(height * bytes_per_line)


            # Edit the bytes
            edited_bytes = bytearray(ptr.asstring())
            for i in range(0, len(edited_bytes), 4):
                r = edited_bytes[i]
                g = edited_bytes[i + 1]
                b = edited_bytes[i + 2]
                a = edited_bytes[i + 3]

                if (r, g, b, a) == self.origin_color:
                    edited_bytes[i] = self.replace_color[0]
                    edited_bytes[i + 1] = self.replace_color[1]
                    edited_bytes[i + 2] = self.replace_color[2]
                    edited_bytes[i + 3] = self.replace_color[3]

            # Create a new QImage from edited bytes
            modified_image = QImage(edited_bytes, width, height, bytes_per_line, QImage.Format_RGBA8888)

            # Cache the modified image and its color settings for future use
            self._image_cache[cache_key] = modified_image

        
        else:
            # If the image is in the cache, use the cached version
            modified_image = self._image_cache[cache_key]

        modified_image = self.transform_modified_image(modified_image)
        return modified_image