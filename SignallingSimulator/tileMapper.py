from tileBase import *
import pyglet
import json
from PyQt5.QtCore import Qt
import math
from extra import WarningBox
from routing import *


class TileMapper:
    def __init__(self, map_draw):

        #Define Variables
        self.map_draw = map_draw
        self.height = 0
        self.width = 0
        self.map_name = ""


        self.tileDimension = 50

        self.highLightedTile = None

        self.autoTrackInitialTile = None
        self.routingInitialTile = None

        self.autoTrackObjects = []
        self.routingObjects = []

        #self.tileBatch = self.openGlInstance.createNewBatch("tileMapper")

    def openFile(self, fileName):

        #Read from the json file
        trackData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.
        self.map_name = trackData["name"]
        self.height = trackData["grid_size"]["rows"]
        self.width = trackData["grid_size"]["columns"]

        #Initialize the tile map
        self.tileMap = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Extract the 'data' field from the trackData dictionary
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

            # Determine the tile type and create the appropriate tile object
            if type == "signalTrack":
                tileObj = SignalTile(self.map_draw, "assets/trackRedSignal.png", point, flip, realCoord,tileCoord)
            elif type == "contTrack":

                tileObj = PortalTile(self.map_draw, "assets/trackContinuation.png", point, flip, realCoord,tileCoord,tile['distance'],self.tileMap,tile.get('connect', None))
            elif type == "platTrack":
                tileObj = TrackTile(self.map_draw, "assets/platform.png", point, flip, realCoord,tileCoord,tile['distance'])
            elif type == "track":
                tileObj = TrackTile(self.map_draw, "assets/trackHorizontal.png", point, flip, realCoord,tileCoord, tile['distance'])
            elif type == "pointTrack":
                tileObj = PointTile(self.map_draw, "assets/pointStraight.png", point, flip, realCoord,tileCoord)
            elif type == "curveTrack":
                tileObj = CurveTile(self.map_draw, "assets/trackCurve.png", point, flip, realCoord,tileCoord,tile['distance'])
            elif type == "bufferTrack":
                tileObj = TrackTile(self.map_draw, "assets/trackBuffer.png", point, flip, realCoord,tileCoord,tile['distance'])
            elif type == "diagonalTrack":
                tileObj = DiagonalTile(self.map_draw, "assets/trackDiagonal.png", point, flip, realCoord,tileCoord,tile['distance'])

            # Assign the created tile object to the appropriate location in the tile map
            self.tileMap[row][column] = tileObj

        # Extract text data from trackData
        textData = trackData['text']

        #Configure the signal tile
        self.signalTileConfigure()

        # # Iterate through each text object in textData
        # for textObject in textData:
        #     # Convert text coordinates to real coordinates on the screen
        #     realCoord = self.tileToCoord((textObject['row'], textObject['column']))

        #     # Create a pyglet text label with specified properties
        #     text_label = pyglet.text.Label(
        #         textObject['text'],
        #         font_name="Arial",
        #         font_size=18,
        #         x=realCoord[0], y=realCoord[1],  # Position of the text label
        #         anchor_x="center", anchor_y="center",  # Anchoring at the center
        #         color=(255, 255, 255, 255),  # Text color in RGBA format (white in this case)
        #         batch=self.tileBatch,
        #     )
        
    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
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

        for i in self.tileMap:
            for tile in i:
                if tile!=None:
                    tile.handleClickOff()
        if 0<=pressedCoord[1]<self.height and 0<=pressedCoord[0]<self.width and self.tileMap[pressedCoord[1]][pressedCoord[0]]!=None:
            self.tileMap[pressedCoord[1]][pressedCoord[0]].handleClick()
            self.handleClickOnTile(self.tileMap[pressedCoord[1]][pressedCoord[0]])

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
