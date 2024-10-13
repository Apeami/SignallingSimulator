from tileBase import *
import json
from PyQt5.QtWidgets import QMessageBox
import math
from extra import WarningBox
from routing import *


class TileMapper:
    def __init__(self, map_draw, clicked_callback = None):

        #Define Variables
        self.map_draw = map_draw
        self.height = 0
        self.width = 0
        self.map_name = ""

        self.clicked_callback = clicked_callback

        self.tileDimension = 50

        self.highLightedTile = None

        self.autoTrackInitialTile = None
        self.routingInitialTile = None

        self.autoTrackObjects = []
        self.routingObjects = []

        #self.tileBatch = self.openGlInstance.createNewBatch("tileMapper")

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText("Error")
        error_dialog.setInformativeText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

    def getTileObj(self, type, point, flip, realCoord, tileCoord, distance, connect):
        # Determine the tile type and create the appropriate tile object
        if type == "signalTrack":
            tileObj = SignalTile(self.map_draw, "RedSignal", point, flip, realCoord,tileCoord)
        elif type == "contTrack":
            tileObj = PortalTile(self.map_draw, "Continuation", point, flip, realCoord,tileCoord,distance,self.tileMap,connect)
        elif type == "platTrack":
            tileObj = TrackTile(self.map_draw, "Platform", point, flip, realCoord,tileCoord,distance)
        elif type == "track":
            tileObj = TrackTile(self.map_draw, "Straight", point, flip, realCoord,tileCoord, distance)
        elif type == "pointTrack":
            tileObj = PointTile(self.map_draw, "PointOpen", point, flip, realCoord,tileCoord)
        elif type == "curveTrack":
            tileObj = CurveTile(self.map_draw, "Curve", point, flip, realCoord,tileCoord,distance)
        elif type == "bufferTrack":
            tileObj = TrackTile(self.map_draw, "Buffer", point, flip, realCoord,tileCoord,distance)
        elif type == "diagonalTrack":
            tileObj = DiagonalTile(self.map_draw, "Diagonal", point, flip, realCoord,tileCoord,distance)
        elif type == "bridgeTrack":
            tileObj = BridgeTile(self.map_draw, "Bridge", point, flip, realCoord,tileCoord,distance)
        return tileObj

    def openFile(self, fileName):
        #Read from the json file
        trackData = self.load_json_from_file(fileName)
        try:
            print(fileName)
            trackData = self.load_json_from_file(fileName)
        except Exception as e:
            self.show_error_message(str(e))
            return True
        return self.openMap(trackData)

    def openMap(self, trackData):

        if "type" not in trackData or trackData["type"]!= "map":
            self.show_error_message("File is not of type: map")
            return True

        #Extract track metadata and dimensions from loaded JSON data.
        if "name" not in trackData:
            self.show_error_message("No map name provided")
            return True
        self.map_name = trackData["name"]

        if "grid_size" not in trackData:
            self.show_error_message("No map height and width provided")
        self.height = trackData["grid_size"]["rows"]
        self.width = trackData["grid_size"]["columns"]
 
        self.map_draw.del_all_tile()
        self.map_draw.setBoundaryPoints(self.width,self.height)

        #Initialize the tile map
        self.tileMap = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Extract the 'data' field from the trackData dictionary
        if "data" not in trackData:
            self.show_error_message("No map data provided")
            return True
        self.map_data = trackData["data"]

        # Iterate through each tile in the map data
        for tile in self.map_data:
            # Extract row and column values for the current tile
            row = tile['row']
            column = tile['column']

            # Convert tile coordinates to real coordinates on the screen
            realCoord = self.tileToCoord((column, row))
            tileCoord = (column,row)

            # Extract properties of the tile
            type = tile['type']
            point = tile['point']
            flip = tile['flip']

            tileObj = self.getTileObj(type, point, flip, realCoord, tileCoord, tile['distance'], tile.get('connect', None))

            # Assign the created tile object to the appropriate location in the tile map
            self.tileMap[row][column] = tileObj

        # Extract blanks
        for rowI in range(len(self.tileMap)):
            row = self.tileMap[rowI]
            for colI in range(len(row)):
                realCoord = self.tileToCoord((colI, rowI))
                tileCoord = (colI,rowI)
                if self.tileMap[rowI][colI] == None:
                    self.tileMap[rowI][colI] = TileBase(self.map_draw, None, None, None, realCoord,tileCoord)

        # Extract text data from trackData
        textData = trackData['text']

        self.map_draw.setText(textData)

        #Configure the signal tile
        self.signalTileConfigure()

        self.trackData = trackData

        return False
        
    #This function opens the file.
    def load_json_from_file(self, file_path):
        print("Load Json")
        print(file_path)
        
        with open(file_path, 'r') as file:
            print("Here")
            json_data = json.load(file)
            print(json_data)
        return json_data
    
    #These convert the pyglet coordinate to the tile map array index
    #It is hardcoded to a value of 50
    def tileToCoord(self, tileLoc):
        return (tileLoc[0]*50, tileLoc[1]*50)
    
    def coordToTile(self, coord):
        return (math.floor(coord[0]/50), math.floor(coord[1]/50)+1)
    
    #When the mouse is pressed a tile is sent a clicked command
    def canvasMousePressEvent(self, mapX, mapY):
        # propX = x/width
        # propY = y/height

        # mapX = left + propX * (right-left)
        # mapY = top + propY * (bottom-top)


        pressedCoord = self.coordToTile((mapX,mapY))

        print("Canvas mouse clicked")
        print(pressedCoord)

        for i in self.tileMap:
            for tile in i:
                if tile!=None:
                    tile.handleClickOff()
        if 0<=pressedCoord[1]<self.height and 0<=pressedCoord[0]<self.width and self.tileMap[pressedCoord[1]][pressedCoord[0]]!=None:
            self.tileMap[pressedCoord[1]][pressedCoord[0]].handleClick()
            self.handleClickOnTile(self.tileMap[pressedCoord[1]][pressedCoord[0]])

            #Callback for clicked
            if self.clicked_callback!=None:
                self.clicked_callback()

    def checkRoutingCompatibility(self,routing):
        if routing.tileList!=None:
            for initroute in self.routingObjects + self.autoTrackObjects:
                    for inittile in initroute.tileList:
                        for comptile in routing.tileList:
                            if inittile!=initroute.firstTile and inittile!=initroute.secondTile and comptile!=routing.firstTile and comptile!=routing.secondTile:
                                if inittile == comptile:
                                    return False
            return True
        else:
            return False

    def handleClickOnTile(self, tile):
        self.highLightedTile = tile
        if self.routingInitialTile!=None:
            firstTile = self.routingInitialTile
            secondTile = self.highLightedTile
            self.routingInitialTile=None

            routing = RoutingTrack(firstTile,secondTile,self)

            if self.checkRoutingCompatibility(routing):
                if routing.success:
                    routing.createRouting()
                    self.routingObjects.append(routing)
                    self.updateRoutings(routing)
            else:
                WarningBox("This routing is over another routing.","Cannot complete").exec_()

        if self.autoTrackInitialTile!=None:
            firstTile = self.autoTrackInitialTile
            secondTile = self.highLightedTile
            self.autoTrackInitialTile = None

            routing = AutoTrack(firstTile,secondTile,self)

            if self.checkRoutingCompatibility(routing):
                if routing.success:
                    routing.createRouting()
                    self.autoTrackObjects.append(routing)
                    self.updateRoutings(routing)
            else:
                WarningBox("This routing is over another routing.","Cannot complete").exec_()

    def updateRoutings(self,centralRouting):
        # for routing in self.autoTrackObjects + self.routingObjects:
        #     routing.delete()
        #     routing.active = True

        # for routing in self.autoTrackObjects:
        #     if routing.firstTile == centralRouting.secondTile or routing.secondTile ==centralRouting.firstTile:
        #         routing.createRouting()
        # if isinstance(centralRouting,AutoTrack):
        #     centralRouting.createRouting()

        # for routing in self.routingObjects:
        #     if routing.firstTile == centralRouting.secondTile or routing.secondTile ==centralRouting.firstTile:
        #         routing.createRouting()
        # if isinstance(centralRouting,RoutingTrack):
        #     centralRouting.createRouting()
    
        for routing in self.autoTrackObjects:
            routing.createRouting()

        for routing in self.routingObjects:
            routing.createRouting()

    #This are used to set the signal of any highlighted tile.
    def setSignal(self,type):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, SignalTile):
                    tile.setSignal(type)
                    #self.updateSignals(tile)

    def updateSignals(self):
        for j in range(4):
            for i in self.tileMap:
                for tile in i:
                    if tile!=None and isinstance(tile, SignalTile):
                        tile.updateSignal()

    def togglePoint(self):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, PointTile):
                    tile.togglePoint()  

    def delete(self):
        #self.openGlInstance.removeBatch("tileMapper")
        self.map_draw.tile_list = []

    def getCoordFromName(self,name):
        for tile in self.map_data:
            if "waypoint" in tile:
                if tile['waypoint']==name:
                    return (tile['row'],tile['column'])
                
    def getNameFromCoord(self,coord):
        for tile in self.map_data:
            if tile['row'] == coord[0] and tile['column'] == coord[1]:
                if "waypoint" in tile:
                    return tile['waypoint']



    def signalTileConfigure(self):
        for row in self.tileMap:
            for column in row:
                if isinstance(column,SignalTile):
                    tile = column
                    tileList = BranchSignalTile(self).getSignalList(tile)


                    tile.nextSignalList = tileList

                    if len(tileList)==0:
                        tile.lastSignal = True

                    tile.updateSignal()

        for row in self.tileMap:
            for column in row:
                if isinstance(column,SignalTile):
                    tile = column
                    for nextSignal in tile.nextSignalList:
                        nextSignal.prevSignalList.append(tile)
                

    def manageAutoTrack(self):
        self.autoTrackInitialTile = self.highLightedTile
        self.routingInitialTile = None

    def manageTrainRoute(self):
        self.autoTrackInitialTile = None
        self.routingInitialTile = self.highLightedTile


    def manageDeleteRouting(self):
        for route in self.autoTrackObjects:
            if route.deleteIfSelected(self.highLightedTile):
                self.updateRoutings(route)
                if route in self.autoTrackObjects:
                    self.autoTrackObjects.remove(route)
        for route in self.routingObjects:
            if route.deleteIfSelected(self.highLightedTile):
                self.updateRoutings(route)
                if route in self.routingObjects:
                    self.routingObjects.remove(route)

    def zoomtopoint(self, loc):
        print("Zooming to")
        print(loc)
        coord = (self.getCoordFromName(loc)[1]*50, self.getCoordFromName(loc)[0]*50)
        self.map_draw.zoomToPoint(coord)