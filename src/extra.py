from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton


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