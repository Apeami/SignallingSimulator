from tileBase import *
import pyglet
import json
from PyQt5.QtCore import Qt
import math


class TileMapper:
    def __init__(self, openGlInstance,shape):

        #Define Variables
        self.openGlInstance = openGlInstance
        self.height = 0
        self.width = 0
        self.map_name = ""
        self.shapes = shape

        self.tileDimension = 50

        self.highLightedTile = None

        self.autoTrackInitialTile = None
        self.routingInitialTile = None

        self.tileBatch = self.openGlInstance.createNewBatch("tileMapper")

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
                tileObj = SignalTile(self.openGlInstance,self.tileBatch, "assets/trackRedSignal.png", point, flip, realCoord,tileCoord)
            elif type == "contTrack":

                tileObj = PortalTile(self.openGlInstance,self.tileBatch, "assets/trackContinuation.png", point, flip, realCoord,tileCoord,tile['distance'],self.tileMap,tile.get('connect', None))
            elif type == "platTrack":
                tileObj = TrackTile(self.openGlInstance,self.tileBatch, "assets/platform.png", point, flip, realCoord,tileCoord,100)
            elif type == "track":
                tileObj = TrackTile(self.openGlInstance, self.tileBatch, "assets/trackHorizontal.png", point, flip, realCoord,tileCoord, tile['distance'])
            elif type == "pointTrack":
                tileObj = PointTile(self.openGlInstance, self.tileBatch, "assets/pointStraight.png", point, flip, realCoord,tileCoord)
            elif type == "curveTrack":
                tileObj = CurveTile(self.openGlInstance, self.tileBatch, "assets/trackCurve.png", point, flip, realCoord,tileCoord,tile['distance'])
            elif type == "bufferTrack":
                tileObj = TrackTile(self.openGlInstance, self.tileBatch, "assets/trackBuffer.png", point, flip, realCoord,tileCoord,tile['distance'])
            elif type == "diagonalTrack":
                tileObj = TrackTile(self.openGlInstance, self.tileBatch, "assets/trackDiagonal.png", point, flip, realCoord,tileCoord,tile['distance'])

            # Assign the created tile object to the appropriate location in the tile map
            self.tileMap[row][column] = tileObj

        # Extract text data from trackData
        textData = trackData['text']

        #Configure the signal tile
        self.signalTileConfigure()

        # Iterate through each text object in textData
        for textObject in textData:
            # Convert text coordinates to real coordinates on the screen
            realCoord = self.tileToCoord((textObject['row'], textObject['column']))

            # Create a pyglet text label with specified properties
            text_label = pyglet.text.Label(
                textObject['text'],
                font_name="Arial",
                font_size=18,
                x=realCoord[0], y=realCoord[1],  # Position of the text label
                anchor_x="center", anchor_y="center",  # Anchoring at the center
                color=(255, 255, 255, 255),  # Text color in RGBA format (white in this case)
                batch=self.tileBatch,
            )
        
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
        return (math.floor(coord[0]/50), math.floor(coord[1]/50))
    
    #When the mouse is pressed a tile is sent a clicked command
    def canvasMousePressEvent(self, x,y,left,right,top,bottom,width,height):
        propX = x/width
        propY = y/height

        mapX = left + propX * (right-left)
        mapY = top + propY * (bottom-top)

        pressedCoord = self.coordToTile((mapX,mapY))

        for i in self.tileMap:
            for tile in i:
                if tile!=None:
                    tile.handleClickOff()
        if 0<=pressedCoord[1]<self.height and 0<=pressedCoord[0]<self.width and self.tileMap[pressedCoord[1]][pressedCoord[0]]!=None:
            self.tileMap[pressedCoord[1]][pressedCoord[0]].handleClick()
            self.handleClickOnTile(self.tileMap[pressedCoord[1]][pressedCoord[0]])

    def handleClickOnTile(self, tile):
        self.highLightedTile = tile
        print(tile.tileCoord)

        if self.routingInitialTile!=None:
            firstTile = self.routingInitialTile
            secondTile = self.highLightedTile
            self.routingInitialTile=None

        if self.autoTrackInitialTile!=None:
            firstTile = self.autoTrackInitialTile
            secondTile = self.highLightedTile
            self.autoTrackInitialTile = None

    #This are used to set the signal of any highlighted tile.
    def setSignal(self,type):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, SignalTile):
                    print("CHanging to: ", type)
                    tile.setSignal(type)

        for j in range(4):
            for i in self.tileMap:
                for tile in i:
                    if tile!=None and isinstance(tile, SignalTile):
                        tile.updateSignal()

    def togglePoint(self):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, PointTile):
                    print("Toggling Point")
                    tile.togglePoint()  

    def delete(self):
        self.openGlInstance.removeBatch("tileMapper")

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

    def findNextSignal(self, tile, tileDirection, visited=None):

        if visited is None:
            visited = set()

        if tile is None or tile.tileCoord in visited:
            return []

        print("FINDING NEXT SIGNAL")
        print("TileLocation")
        print(tile.tileCoord)
        print("Search Direction")
        print(tileDirection)

        visited.add(tile.tileCoord)

        if isinstance(tile, SignalTile):
            print("ReturningTile")
            print(tile.tileCoord)
            return [tile]

        entryDir = (-tileDirection[0], -tileDirection[1])
        coords = tile.getEntryAndExitCoord()

        print("directional Coords")
        print(coords)
        print("entry Dir")
        print(entryDir)

        tileList = []
        for coord in coords:
            if coord != entryDir:
                newTileCoordX = tile.tileCoord[0] + coord[1]
                newTileCoordY = tile.tileCoord[1] + coord[0]

                newTile = self.tileMap[newTileCoordY][newTileCoordX]
                print("Calling Function")
                print("Direction Coord")
                print(coord)
                print("X")
                print(newTileCoordX)
                print("Y")
                print(newTileCoordY)
                result = self.findNextSignal(newTile, coord, visited)
                #result = []
                for i in result:
                    tileList.append(i)

        return tileList




    def signalTileConfigure(self):
        print("SignalTileConfig")
        for row in self.tileMap:
            for column in row:
                if isinstance(column,SignalTile):
                    tile = column
                    startDir = tile.getDefaultStartDir()
                    entryLoc = (startDir[0],startDir[1])
                    newTile = self.tileMap[tile.tileCoord[1]+startDir[0]][tile.tileCoord[0]+startDir[1]]
                    tileList = self.findNextSignal(newTile,entryLoc)

                    print("SIGNAL OUTPUT")
                    print("InputTile")
                    print(tile.tileCoord)
                    print("OUTPUT TILE LIST")
                    for item in tileList:
                        print(item.tileCoord)
                    print("End of SIGNAL tile config")

                    tile.nextSignalList = tileList

                    if len(tileList)==0:
                        tile.lastSignal = True

                    tile.updateSignal()
                

    def manageAutoTrack(self):
        self.autoTrackInitialTile = self.highLightedTile

    def manageTrainRoute(self):
        self.routingInitialTile = self.highLightedTile

    def manageDeleteRouting(self):
        print("Managing delete route")