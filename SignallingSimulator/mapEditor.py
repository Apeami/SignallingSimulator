from PyQt5.QtWidgets import QWidget, QFileDialog

import ui_mapEditor 
from tileMapper import TileMapper
from timetableEditor import TimetableEditor
import json

class MapEditor(ui_mapEditor.Ui_Form):
    def __init__(self, fileName, newFile, openTimetableEditor):
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)

        self.fileName = fileName
        self.mainWidget.show()

        self.tileMapper = TileMapper(self.MapWidget)

        if newFile:
            self.trackData = self.createSkeletonMap()
            self.tileMapper.openMap(self.trackData)
        else:
            self.tileMapper.openFile(self.fileName)
            self.trackData = self.tileMapper.trackData

        self.MapWidget.mousePressSignal.connect(self.tileMapper.canvasMousePressEvent)
        self.MapWidget.zoomToActualSize(self.tileMapper)

        self.TrackButton.clicked.connect(lambda: self.changeTileType("track"))
        self.DiagonalTrackButton.clicked.connect(lambda: self.changeTileType("diagonalTrack"))
        self.CurveTrackButton.clicked.connect(lambda: self.changeTileType("curveTrack"))
        self.SignalButton.clicked.connect(lambda: self.changeTileType("signalTrack"))
        self.PointButon.clicked.connect(lambda: self.changeTileType("pointTrack"))
        self.PlatformButton.clicked.connect(lambda: self.changeTileType("platTrack"))
        self.BufferButton.clicked.connect(lambda: self.changeTileType("bufferTrack"))
        self.EndPortalButton.clicked.connect(lambda: self.changeTileType("contTrack"))

        self.EastButton.clicked.connect(lambda: self.changeTileRotation('east'))
        self.WestButton.clicked.connect(lambda: self.changeTileRotation('west'))
        self.NorthButton.clicked.connect(lambda: self.changeTileRotation('north'))
        self.SouthButton.clicked.connect(lambda: self.changeTileRotation('south'))

        self.ToggleFlipButton.clicked.connect(lambda: self.flipTile())

        self.SaveButton.clicked.connect(lambda: self.saveMap(fileName))

        self.NewTimetableButton.clicked.connect(lambda: TimetableEditor().show())
        self.EditTimetableButton.clicked.connect(lambda: openTimetableEditor(False, self.trackData["name"]))

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
        self.MapWidget.mousePressSignal.connect(self.tileMapper.canvasMousePressEvent)
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