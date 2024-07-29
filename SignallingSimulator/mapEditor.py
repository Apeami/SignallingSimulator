from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow, QMessageBox

from ui_MapEditor import Ui_MainWindow 
from tileMapper import TileMapper
from timetableEditor import TimetableEditor
import json

class MapEditor(QMainWindow):
    def __init__(self, appMain):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signalling Simulator")
        self.show()

        self.editing = False

        self.ui.actionOpen_Map_Player.triggered.connect(appMain.playButton)
        self.ui.actionNew_Map.triggered.connect(lambda: self.openMap(True))
        self.ui.actionEdit_Map.triggered.connect(lambda: self.openMap(False))

        self.timeTableEditor = TimetableEditor(self)



    def openMapConfirmation(self, message):
        confirm_box = QMessageBox(self)
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setWindowTitle('Confirmation')
        confirm_box.setText(message)
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        button_clicked = confirm_box.exec_()

        if button_clicked == QMessageBox.No:
            return True
        return False

    def openMap(self, isNew):
        if self.editing:
            if self.openMapConfirmation('You are already editing a map, are you sure you want to open another one?'):
                return
        
        if not isNew:
            self.fileName = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
            if self.fileName==('', ''):
                return
        else:
            self.fileName = None

        self.editing = True

        self.tileMapper = TileMapper(self.ui.MapWidget)

        if isNew:
            self.trackData = self.createSkeletonMap()
            self.tileMapper.openMap(self.trackData)
        else:
            self.tileMapper.openFile(self.fileName)
            self.trackData = self.tileMapper.trackData

        self.ui.MapWidget.mousePressSignal.connect(self.tileMapper.canvasMousePressEvent)
        self.ui.MapWidget.zoomToActualSize(self.tileMapper)

        self.ui.TrackButton.clicked.connect(lambda: self.changeTileType("track"))
        self.ui.DiagonalTrackButton.clicked.connect(lambda: self.changeTileType("diagonalTrack"))
        self.ui.CurveTrackButton.clicked.connect(lambda: self.changeTileType("curveTrack"))
        self.ui.SignalButton.clicked.connect(lambda: self.changeTileType("signalTrack"))
        self.ui.PointButon.clicked.connect(lambda: self.changeTileType("pointTrack"))
        self.ui.PlatformButton.clicked.connect(lambda: self.changeTileType("platTrack"))
        self.ui.BufferButton.clicked.connect(lambda: self.changeTileType("bufferTrack"))
        self.ui.EndPortalButton.clicked.connect(lambda: self.changeTileType("contTrack"))

        self.ui.EastButton.clicked.connect(lambda: self.changeTileRotation('east'))
        self.ui.WestButton.clicked.connect(lambda: self.changeTileRotation('west'))
        self.ui.NorthButton.clicked.connect(lambda: self.changeTileRotation('north'))
        self.ui.SouthButton.clicked.connect(lambda: self.changeTileRotation('south'))

        self.ui.ToggleFlipButton.clicked.connect(lambda: self.flipTile())

        self.ui.actionSave.triggered.connect(lambda: self.saveMap(fileName))

        self.ui.actionNew_Timetable.triggered.connect(lambda: self.timeTableEditor.open(True))
        self.ui.actionEditTimetable.triggered.connect(lambda: self.timeTableEditor.open(False))

    def openAttributesWindow(self):
        pass

    def saveMap(self, filePath):
        
        if filePath == None:
            filePath = QFileDialog.getSaveFileName(self.mainWidget, "Create New File", "", "All Files (*);;Text Files (*.txt)")

        print(self.trackData)
        print(filePath[0])

        with open(filePath[0], 'w') as file:
            json.dump(self.trackData, file, indent=4)


    def createSkeletonMap(self):
        map = {}
        map["type"]= "map"
        map["name"] = "TODOTEMPNAME"

        map["grid_size"] = {
            "rows": 10,
            "columns": 10
        }
        map["data"] = [{ "row": 0, "column": 0, "type": "signalTrack", "point": "west","flip":False,"distance":56 }]
        map['text'] = []
        return map
    
    def getSelectedTile(self):
        for rowI in range(len(self.tileMapper.tileMap)):
            row = self.tileMapper.tileMap[rowI]
            for colI in range(len(row)):
                tile = row[colI]
                if tile == self.tileMapper.highLightedTile:
                    return colI, rowI
        return None,None

    def reDrawMap(self):
        prevSelect = self.tileMapper.highLightedTile.tileCoord
        self.tileMapper.openMap(self.trackData)
        self.ui.MapWidget.mousePressSignal.connect(self.tileMapper.canvasMousePressEvent)
        self.tileMapper.handleClickOnTile(self.tileMapper.tileMap[prevSelect[1]][prevSelect[0]])

    def changeTileRotation(self, dir):
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    data['point'] = dir

        self.reDrawMap()

    def flipTile(self):
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    if data['flip'] == False:
                        data['flip'] = True
                    else:
                        data['flip'] = False

        self.reDrawMap()

    def changeTileType(self,tileType):
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            exist = False
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    data['type'] = tileType
                    exist = True

            if exist ==False:
                default_data = { "row": rowI, "column": colI, "type": tileType, "point": "east","flip":False,"distance":100 }
                self.trackData['data'].append(default_data)

        self.reDrawMap()