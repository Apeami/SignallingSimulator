from tileBase import *
import pyglet
import json
from PyQt5.QtCore import Qt
import math


class TileMapper:

    def __init__(self, openGlInstance,shape):
        self.openGlInstance = openGlInstance

        self.height = 0
        self.width = 0
        self.map_name = ""


        self.shapes = shape

    def openFile(self, fileName):
        trackData = self.load_json_from_file(fileName)

        self.map_name = trackData["name"]
        self.height = trackData["grid_size"]["rows"]
        self.width = trackData["grid_size"]["columns"]

        self.tileMap = [[None for _ in range(self.width)] for _ in range(self.height)]

        map_data = trackData["data"]

        for tile in map_data:
            row = tile['row']
            column = tile['column']


            realCoord = self.tileToCoord((column,row))

            type = tile['type']
            point = tile['point']
            flip = tile['flip']


            if tile['type']=="signalTrack":
                tileObj = SignalTile(self.openGlInstance,"assets/trackRedSignal.png",point,flip,realCoord)
            if tile['type']=="contTrack":
                tileObj = TileBase(self.openGlInstance,"assets/trackContinuation.png",point,flip,realCoord)
            if tile['type']=="platTrack":
                tileObj = TileBase(self.openGlInstance,"assets/platform.png",point,flip,realCoord)
            if tile['type']=="track":
                tileObj = TileBase(self.openGlInstance,"assets/trackHorizontal.png",point,flip,realCoord)
            if tile['type']=="pointTrack":
                tileObj = PointTile(self.openGlInstance,"assets/pointStraight.png",point,flip,realCoord)
            if tile['type']=="curveTrack":
                tileObj = TileBase(self.openGlInstance,"assets/trackCurve.png",point,flip,realCoord)
            if tile['type']=="bufferTrack":
                tileObj = TileBase(self.openGlInstance,"assets/trackBuffer.png",point,flip,realCoord)


            self.tileMap[row][column] = tileObj

        print(self.map_name)
        print(self.tileMap)

        #Manage text
        textData = trackData['text']
        for textObject in textData:
            realCoord = self.tileToCoord((textObject['row'],textObject['column']))
            text_label = pyglet.text.Label(
                textObject['text'],
                font_name="Arial",
                font_size=18,
                x=realCoord[0], y=realCoord[1],  # Position of the text label
                anchor_x="center", anchor_y="center",  # Anchoring at the center
                color=(255, 255, 255, 255),  # Text color in RGBA format (white in this case)
                batch=self.openGlInstance.batch,
            )
        

    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data
    
    def tileToCoord(self, tileLoc):
        return (tileLoc[0]*50, tileLoc[1]*50)
    
    def coordToTile(self, coord):
        return (math.floor(coord[0]/50), math.floor(coord[1]/50))
    
    def canvasMousePressEvent(self, x,y,left,right,top,bottom,width,height):
        print(f"Mouse pressed at ({x}, {y})")
        propX = x/width
        propY = y/height

        mapX = left + propX * (right-left)
        mapY = top + propY * (bottom-top)

        print(mapX,mapY)

        pressedCoord = self.coordToTile((mapX,mapY))

        print(pressedCoord)

        print(self.width)
        print(self.height)

        for i in self.tileMap:
            for tile in i:
                if tile!=None:
                    tile.handleClickOff()
        if 0<=pressedCoord[1]<self.height and 0<=pressedCoord[0]<self.width and self.tileMap[pressedCoord[1]][pressedCoord[0]]!=None:
            self.tileMap[pressedCoord[1]][pressedCoord[0]].handleClick()

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
