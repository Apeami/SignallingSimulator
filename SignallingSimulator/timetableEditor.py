
import ui_timetableEditor
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class TimetableEditor(QWidget):
    def __init__(self):
        super().__init__()
        print("NEWWINDOW")
        self.setWindowTitle("New Window")
        self.setGeometry(150, 150, 300, 200)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("This is a new window")
        self.layout.addWidget(self.label)
        
        self.setLayout(self.layout)

# class TimetableEditor(ui_timetableEditor.Ui_Form):
#     def __init__(self, fileNameNew, mapName):
#         print("OPEN TIMETABEL")
#         self.mainWidget = QWidget()
#         self.setupUi(self.mainWidget)
#         self.mainWidget.show()

#         self.mapName = mapName

#         print("DONE")
