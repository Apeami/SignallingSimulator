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


            if tile['type']=="signalTrack":
                tileObj = SignalTile(self.openGlInstance,"assets/trackRedSignal.png",point,realCoord)
            if tile['type']=="contTrack":
                tileObj = TileBase(self.openGlInstance,"assets/trackContinuation.png",point,realCoord)
            if tile['type']=="platTrack":
                tileObj = TileBase(self.openGlInstance,"assets/platform.png",point,realCoord)
            if tile['type']=="track":
                tileObj = TileBase(self.openGlInstance,"assets/trackHorizontal.png",point,realCoord)
            if tile['type']=="pointTrack":
                tileObj = TileBase(self.openGlInstance,"assets/pointStraight.png",point,realCoord)


            self.tileMap[row][column] = tileObj

        print(self.map_name)
        print(self.tileMap)

        

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
