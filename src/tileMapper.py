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
        map_data = trackData["data"]

        # Iterate through each tile in the map data
        for tile in map_data:
            # Extract row and column values for the current tile
            row = tile['row']
            column = tile['column']

            # Convert tile coordinates to real coordinates on the screen
            realCoord = self.tileToCoord((column, row))

            # Extract properties of the tile
            type = tile['type']
            point = tile['point']
            flip = tile['flip']

            # Determine the tile type and create the appropriate tile object
            if type == "signalTrack":
                tileObj = SignalTile(self.openGlInstance, "assets/trackRedSignal.png", point, flip, realCoord)
            elif type == "contTrack":
                tileObj = TileBase(self.openGlInstance, "assets/trackContinuation.png", point, flip, realCoord)
            elif type == "platTrack":
                tileObj = TileBase(self.openGlInstance, "assets/platform.png", point, flip, realCoord)
            elif type == "track":
                tileObj = TrackTile(self.openGlInstance, "assets/trackHorizontal.png", point, flip, realCoord, tile['distance'])
            elif type == "pointTrack":
                tileObj = PointTile(self.openGlInstance, "assets/pointStraight.png", point, flip, realCoord)
            elif type == "curveTrack":
                tileObj = TileBase(self.openGlInstance, "assets/trackCurve.png", point, flip, realCoord)
            elif type == "bufferTrack":
                tileObj = TileBase(self.openGlInstance, "assets/trackBuffer.png", point, flip, realCoord)

            # Assign the created tile object to the appropriate location in the tile map
            self.tileMap[row][column] = tileObj

        # Extract text data from trackData
        textData = trackData['text']

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
                batch=self.openGlInstance.batch,
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

    #This are used to set the signal of any highlighted tile.
    def setSignal(self,type):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, SignalTile):
                    print("CHanging to: ", type)
                    tile.setSignal(type)

    def togglePoint(self):
        for i in self.tileMap:
            for tile in i:
                if tile!=None and tile.highlighted==True and isinstance(tile, PointTile):
                    print("Toggling Point")
                    tile.togglePoint()  