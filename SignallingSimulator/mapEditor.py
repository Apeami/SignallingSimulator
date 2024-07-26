from PyQt5.QtWidgets import QWidget

import ui_mapEditor 
from tileMapper import TileMapper

class MapEditor(ui_mapEditor.Ui_Form):
    def __init__(self, fileName):
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)

        self.fileName = fileName
        self.mainWidget.show()

        self.tileMapper = TileMapper(self.MapWidget)
        self.tileMapper.openFile(self.fileName)
        self.MapWidget.mousePressSignal.connect(self.tileMapper.canvasMousePressEvent)
        self.MapWidget.zoomToActualSize(self.tileMapper)