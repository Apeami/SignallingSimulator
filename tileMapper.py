from tileBase import TileBase
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

        map_data = trackData["data"]

        for tile in map_data:
            row = tile['row']
            column = tile['column']

            realCoord = self.tileToCoord((column,row))

            type = tile['type']

            if 'signal' in tile: #This tile is a signal tile
                if tile['type']=="straight":
                    TileBase(self.openGlInstance,"assets/trackRedSignal.png",False,False,False,realCoord)
            elif tile['type']=="deco": #This tile is a decoration block
                if tile['item']=="platform":
                    TileBase(self.openGlInstance,"assets/platform.png",False,False,False,realCoord)
            else: #This tile is regular track
                if tile['type']=="straight":
                    TileBase(self.openGlInstance,"assets/trackHorizontal.png",False,False,False,realCoord)

            print(row)
            print(column)
        print(self.map_name)

        

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

        print(self.coordToTile((mapX,mapY)))