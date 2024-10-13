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
        self.tileMapper =None

        self.ui.actionOpen_Map_Player.triggered.connect(appMain.playButtonCallback)
        self.ui.actionNew_Map.triggered.connect(lambda: self.openMap(True))
        self.ui.actionEdit_Map.triggered.connect(lambda: self.openMap(False))

        self.timeTableEditor = TimetableEditor(self)

        self.ui.actionNew_Timetable.triggered.connect(lambda: self.timeTableEditor.open(True))
        self.ui.actionEditTimetable.triggered.connect(lambda: self.timeTableEditor.open(False))



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
            self.fileName = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")[0]
            if self.fileName=='':
                return
        else:
            self.fileName = None

        print("AFTER OPEN")
        print(self.fileName)

        self.editing = True

        if self.tileMapper!=None:
            self.tileMapper.delete()

        self.tileMapper = TileMapper(self.ui.MapWidget, clicked_callback=self.updateTileAttributes)

        if isNew:
            self.trackData = self.createSkeletonMap()
            self.tileMapper.openMap(self.trackData)
        else:
            self.tileMapper.openFile(self.fileName)
            self.trackData = self.tileMapper.trackData

        self.ui.nameBox.setText(self.trackData['name'])
        self.ui.widthBox.setValue(self.trackData['grid_size']['rows'])
        self.ui.hightBox.setValue(self.trackData['grid_size']['columns'])

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
        self.ui.BridgeButton.clicked.connect(lambda: self.changeTileType("bridgeTrack"))
        self.ui.DeleteButton.clicked.connect(lambda: self.delTile())

        self.ui.EastButton.clicked.connect(lambda: self.changeTileRotation('east'))
        self.ui.WestButton.clicked.connect(lambda: self.changeTileRotation('west'))
        self.ui.NorthButton.clicked.connect(lambda: self.changeTileRotation('north'))
        self.ui.SouthButton.clicked.connect(lambda: self.changeTileRotation('south'))

        self.ui.ToggleFlipButton.clicked.connect(lambda: self.flipTile())

        self.ui.waypointButton.clicked.connect(lambda: self.setTileWaypoint())
        self.ui.distanceButton.clicked.connect(lambda: self.setTileDistance())

        self.ui.updateSizeButton.clicked.connect(self.updateSize)

        self.ui.actionSave.triggered.connect(lambda: self.saveMap())



    def saveMap(self):
        
        self.trackData["name"] = self.ui.nameBox.text()

        if self.fileName == None:
            self.fileName = QFileDialog.getSaveFileName(self, "Create New File", "", "All Files (*);;Text Files (*.txt)")[0]

        print("Saving map")
        print(self.fileName)

        with open(self.fileName, 'w') as file:
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
                    print("Flipping")
                    if data['flip'] == False:
                        data['flip'] = True
                    else:
                        data['flip'] = False

        self.reDrawMap()

    def delTile(self):
        colI, rowI= self.getSelectedTile()
        if colI is not None and rowI is not None:
            print("Deleting")
            print(self.trackData['data'])
            self.trackData['data'] = [data for data in self.trackData['data'] if not (data['row'] == rowI and data['column'] == colI)]
            print(self.trackData['data'])
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

    def setTileDistance(self):
        distance = self.ui.distanceText.text()
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    data['distance'] = int(distance)

    def setTileWaypoint(self):
        waypoint = self.ui.waypointText.text()
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    data['waypoint'] = waypoint

    def updateSize(self):
        width = self.ui.widthBox.value()
        height = self.ui.hightBox.value()
        self.trackData["grid_size"] = {
            "rows": width,
            "columns": height
        }
        self.reDrawMap()

    def updateTileAttributes(self):
        print("updating tile attributes")
        colI, rowI= self.getSelectedTile()
        if colI !=None and rowI!=None:
            for data in self.trackData['data']:
                if data['row'] == rowI and data['column']==colI:
                    self.ui.waypointText.setText(data.get('waypoint', ""))
                    self.ui.distanceText.setText(str(data.get('distance', "")))

