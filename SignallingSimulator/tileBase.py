import random
import math
from extra import ReplacableImage
from DrawMapTile import DrawMapTile
from PyQt5.QtGui import QColor

class TileBase:
    def __init__(self, map_draw, imagetype, point,flip ,location,tileCoord,clickable=False):

       #Image creation
        # image = ReplacableImage(imagePath)
        # image.set_replacement_color((255,255,255,255))
        #image = pyglet.image.load(imagePath)

        #Variable and constant creation
        self.imagetype = imagetype
        # self.width = image.width
        # self.height = image.height
        self.point = point
        self.convert = {"north":270,"east":0,"south":90,"west":180}
        self.highlighted = False
        self.highlight=None
        self.map_draw = map_draw
        self.location = location
        self.flip=flip
        self.tileCoord = tileCoord
        self.tileLoc = (math.floor(self.location[0]/50), math.floor(self.location[1]/50))
        self.color = (255,255,255,255)

        self.draw()

        #Sprite managment

        # if self.flip:
        #     image = image.get_texture().get_transform(flip_y=True)  

        # self.sprite = pyglet.sprite.Sprite(image, batch=self.batch)

        # self.sprite.anchor_x = self.width // 2
        # self.sprite.anchor_y = self.height // 2

        # locationEdited = [self.location[0],self.location[1]]
        # if self.width>50:
        #     locationEdited[0] = locationEdited[0] - ((self.width-50)/2)
        # if self.height>50:
        #     locationEdited[1] = locationEdited[1] - ((self.height-50)/2)

        # self.locationEdited = locationEdited

        # image.flip = self.flip
        # image.point = self.convert[self.point]

        # if self.point=="west":
        #     if self.flip:
        #         locationEdited[1]=locationEdited[1]-self.height
        #     self.sprite.update(locationEdited[0]+self.width, locationEdited[1]+self.height)
        # if self.point=="east":
        #     if self.flip:
        #         locationEdited[1]=locationEdited[1]+self.height
        #     self.sprite.update(locationEdited[0], locationEdited[1])
        # if self.point=="north":
        #     if self.flip:
        #         locationEdited[0]=locationEdited[0]-self.width
        #     self.sprite.update(locationEdited[0]+self.width, locationEdited[1])
        # if self.point=="south":
        #     if self.flip:
        #         locationEdited[0]=locationEdited[0]+self.width
        #     self.sprite.update(locationEdited[0], locationEdited[1]+self.height)

        # self.sprite.rotation = self.convert[point]


        # self.map_draw.shapes.append(self.sprite)
        # self.map_draw.draw_tile(self.locationEdited,image)

    def draw(self):
        if self.imagetype!=None:
            self.tile = DrawMapTile(self.flip, self.point, self.imagetype , QColor(255,255,255))
            self.map_draw.draw_tile(self.location,self.tile)

        
    def changeColor(self, color):
        self.color = color
        # new_image = ReplacableImage(self.imagePath)
        # new_image.set_replacement_color(color)
        #new_image = new_image.render()

        # if self.flip:
        #     new_image = new_image.get_texture().get_transform(flip_y=True)  

        # self.sprite.image = new_image

        self.tile.color = color
        self.map_draw.update()

        # new_image.flip = self.flip
        # new_image.point = self.convert[self.point]
        

        # self.map_draw.draw_tile(self.locationEdited,new_image)

    def remove_from_batch(self):
        self.sprite.delete()

    def handleClick(self):

        if self.highlighted==True:
            self.handleClickOff()
        else:
            # image = pyglet.image.load("Assets/select.png")
            # self.highlight = pyglet.sprite.Sprite(image, batch=self.batch)
            # self.highlight.update(self.location[0], self.location[1])
            # self.map_draw.shapes.append(self.highlight)
            self.map_draw.select_visible = True
            self.map_draw.select_pos = self.location
            self.highlighted=True
            self.map_draw.update()

    def handleClickOff(self):
        self.map_draw.select_visible=False
        self.highlighted = False
        self.map_draw.update()
        # if self.highlight != None:
        #     self.highlight.delete()
        #     self.highlighted = False
        #     self.highlight=None


class TrackTile(TileBase):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord,distance, clickable=False,dimension = 50):
        super().__init__(map_draw, imagePath, point,flip ,location,tileCoord, clickable)
        self.distance = distance
        self.dimension = dimension



    def getWorldCoordFromProgress(self, progress, startDir):

        if startDir == (0,-1):
            self.startCoord = (self.location[0] - self.dimension/2, self.location[1])
            self.endCoord = (self.location[0] + self.dimension/2, self.location[1])
        elif startDir == (0,1):
            self.startCoord = (self.location[0] + self.dimension/2, self.location[1])
            self.endCoord = (self.location[0] - self.dimension/2, self.location[1])
        elif startDir == (-1,0):
            self.startCoord = (self.location[0], self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0], self.location[1] + self.dimension/2)
        elif startDir == (1,0):
            self.startCoord = (self.location[0], self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0], self.location[1] - self.dimension/2)
        elif startDir == (-1,-1):
            self.startCoord = (self.location[0]- self.dimension/2, self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0]+ self.dimension/2, self.location[1] + self.dimension/2)
        elif startDir == (1,1):
            self.startCoord = (self.location[0]+ self.dimension/2, self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0]- self.dimension/2, self.location[1] - self.dimension/2)
        elif startDir == (-1,1):
            self.startCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)
        elif startDir == (1,-1):
            self.startCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)


        current_x = self.startCoord[0] + (self.endCoord[0] - self.startCoord[0]) * progress
        current_y = self.startCoord[1] + (self.endCoord[1] - self.startCoord[1]) * progress
        return (current_x, current_y)

    def getEntryAndExitCoord(self,entryDir = None, currentStatus = False):
        if self.point=="east" or self.point=="west":
            return((0,1),(0,-1))
        elif self.point=="north" or self.point=="south":
            return((1,0),(-1,0))

    def getDefaultStartDir(self):
        if self.point =="east":
            return (0,1)
        if self.point =="west":
            return (0,-1)
        if self.point =="south":
            return (-1,0)
        if self.point =="north":
            return (1,0)
        
    def getNextTileAdd(self,startDir):
        return (-startDir[0],-startDir[1])
        # if startDir == (0,1):
        #     return (0,-1)
        # elif startDir == (0,-1):
        #     return (0,1)
        # elif startDir == (1,0):
        #     return (-1,0)
        # elif startDir == (-1,0):
        #     return (1,0)
        # else:
        #     return (0,0)
        

class BridgeTile(TrackTile):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord,distance, clickable=False,dimension = 50):
        super().__init__(map_draw,imagePath,point,flip,location,tileCoord,distance)

    def getEntryAndExitCoord(self,entryDir = None, currentStatus = False):
        print("Bridge tile ACCESSED")
        print(entryDir)
        if entryDir in ((0,1),(0,-1)):
            return ((0,1),(0,-1))
        if entryDir in ((1,0),(-1,0)):
            return ((1,0),(-1,0))

        # if self.point=="east" or self.point=="west":
        #     return((0,1),(0,-1))
        # elif self.point=="north" or self.point=="south":
        #     return((1,0),(-1,0))

class DiagonalTile(TrackTile):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord,distance, clickable=False,dimension = 50):
        super().__init__(map_draw,imagePath,point,flip,location,tileCoord,distance)

    def getEntryAndExitCoord(self,entryDir = None, currentStatus = False):
        if self.point=="east":
            return((1,1),(-1,-1))
        elif self.point=="west":
            return((1,-1),(-1,1))

class SignalTile(TrackTile):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord, clickable=False, signal="Red"):
        super().__init__(map_draw, imagePath, point,flip ,location,tileCoord,100, clickable)
        self.signal = signal
        self.desiredSignal =signal

        self.lastSignal = False
        self.leaveSignal = False

        self.trainInBlock = False

        self.firstRouteSignal = False
        self.lastRouteSignal = False

        self.trianPassedFunc = None

        self.lock = False #Decreped

        self.nextSignalList = []

        self.prevSignalList = []

    #Changes the signal due to train movements
    def updateSignal(self):
        signalWeight = {"Red":4,"Yellow":3,"DYellow":2,"Green":1}
        reverseSignalWeight = {4:"Red",3:"Yellow",2:"DYellow",1:"Green"}

        modifiedDesiredSignal = self.desiredSignal

        print("Updating Singal")
        print(self.trainInBlock)
        print(self.lastSignal)

        if self.trainInBlock ==True:
            modifiedDesiredSignal = "Red"
        elif self.lastSignal ==True:
            if self.desiredSignal!="Red":
                modifiedDesiredSignal = "Yellow"
        elif self.leaveSignal ==True:
            modifiedDesiredSignal = "Green"
        elif self.firstRouteSignal ==True:
            modifiedDesiredSignal = "Green"
        elif self.lastRouteSignal ==True:
            modifiedDesiredSignal ="Red"
        

        maxWeight = 0
        for signalTile in self.nextSignalList:
            nextSignalstate = signalTile.signal
            nextSignalWeight = signalWeight[nextSignalstate]
            if nextSignalWeight>maxWeight:
                maxWeight=nextSignalWeight

        currentSignalWeight = maxWeight - 1
        if currentSignalWeight<1:
            currentSignalWeight=1

        if signalWeight[modifiedDesiredSignal]>currentSignalWeight:
            currentSignalWeight = signalWeight[modifiedDesiredSignal]
            
        currentSignal = reverseSignalWeight[currentSignalWeight]

        if self.signal !=currentSignal:
            self.setSignalValue(currentSignal)
            for prevSignal in self.prevSignalList:
                prevSignal.updateSignal()

        elif self.signal == currentSignal:
            pass
            
    def trainPassed(self):
        if self.trianPassedFunc!=None:
            self.trianPassedFunc()

    def setTrainPassedAlert(self,function):
        self.trianPassedFunc = function

    def setSignal(self,signal,source = "User"):
        if (source =="Router" and self.lock ==True) or self.lock ==False:
            print("Updating Signal")
            print(signal)
            self.desiredSignal = signal
            self.updateSignal()

    def setSignalValue(self,signal):
        self.signal = signal

        if signal == "Green":
            self.tile.tileType = "GreenSignal"
        elif signal == "DYellow":
            self.tile.tileType = "DYellowSignal"
        elif signal == "Yellow":
            self.tile.tileType = "YellowSignal"
        elif signal == "Red":
            self.tile.tileType = "RedSignal"
        else:
            self.tile.tileType = "RedSignal"

        self.map_draw.draw_tile(self.location,self.tile)
        self.map_draw.update()
        #new_image = pyglet.image.load(newImagePath)
        # new_image = ReplacableImage(newImagePath)
        # new_image.set_replacement_color(self.color)

        # new_image.flip = self.flip
        # new_image.point = self.convert[self.point]
        
        # self.imagePath = newImagePath

        # self.map_draw.draw_tile(self.locationEdited,new_image)

        # if self.flip:
        #     new_image = new_image.get_texture().get_transform(flip_y=True)  

        # self.sprite.image = new_image


class CurveTile(TrackTile):
    def __init__(self, map_draw, imagePath, point, flip,location,distance,tileCoord, clickable=False):
        super().__init__(map_draw, imagePath, point,flip ,location,distance,tileCoord, clickable)
        self.exit = None

    def getEntryAndExitCoord(self,entryDir=None, currentStatus = False):
        entry = super().getDefaultStartDir()
        noDiverge = (-entry[0],-entry[1])

        if self.flip ==True and (self.point=="east"):
            diverge = (-1,1)
        if self.flip ==False and (self.point=="east"):
            diverge = (1,1)
        if self.flip ==True and (self.point=="west"):
            diverge = (1,-1)
        if self.flip ==False and (self.point=="west"):
            diverge = (-1,-1)
        if self.flip ==True and (self.point=="north"):
            diverge = (1,1)
        if self.flip ==False and (self.point=="north"):
            diverge = (1,-1)
        if self.flip ==True and (self.point=="south"):
            diverge = (-1,-1)
        if self.flip ==False and (self.point=="south"):
            diverge = (-1,1)

        return(noDiverge,diverge)
    

    def getWorldCoordFromProgress(self, progress, startDir):
        EntryA, EntryB = CurveTile.getEntryAndExitCoord(self)

        if EntryA == startDir:
            exit = EntryB
            entry = EntryA
        elif EntryB == startDir:
            exit = EntryA 
            entry = EntryB
        else:
            exit = (0,0)
            entry = (0,0)

        
        self.exit = exit
        self.startCoord = (self.location[0] +(entry[1]*self.dimension/2), self.location[1] +(entry[0]*self.dimension/2))
        self.endCoord = (self.location[0] +(exit[1]*self.dimension/2), self.location[1] +(exit[0]*self.dimension/2))
        #midCoord = self.location


        if progress<0.5:
            current_x = self.startCoord[0] + (self.location[0] - self.startCoord[0]) * (progress*2)
            current_y = self.startCoord[1] + (self.location[1] - self.startCoord[1]) * (progress*2)
        elif progress>=0.5:
            current_x = self.location[0] + (self.endCoord[0] - self.location[0]) * ((progress-0.5)*2)
            current_y = self.location[1] + (self.endCoord[1] - self.location[1]) * ((progress-0.5)*2)

        return (current_x, current_y)
    
    def getNextTileAdd(self, startDir):
        return self.exit

class PointTile(CurveTile):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord, clickable=False, diverge=False):
        super().__init__(map_draw, imagePath, point,flip ,location,tileCoord,50, clickable)
        self.diverge=diverge

    def updatePoint(self,diverge):
        self.diverge = diverge

        if not self.diverge:
            self.tile.tileType = "PointOpen"
        else:
            self.tile.tileType = "PointClose"

        self.map_draw.draw_tile(self.location,self.tile)
        self.map_draw.update()
        #new_image = pyglet.image.load(newImagePath)
        # new_image = ReplacableImage(newImagePath)
        # new_image.set_replacement_color(self.color)
        # #new_image = new_image.render()
        # new_image.flip = self.flip
        # new_image.point = self.convert[self.point]
        
        # self.map_draw.draw_tile(self.locationEdited,new_image)


        # self.imagePath = newImagePath
        # if self.flip:
        #     new_image = new_image.get_texture().get_transform(flip_y=True)  

        # self.sprite.image = new_image

    def togglePoint(self):
        if self.diverge==True:
            self.updatePoint(False)
        elif self.diverge==False:
            self.updatePoint(True)


    def getWorldCoordFromProgress(self, progress, startDir):
        if self.diverge:
            return super().getWorldCoordFromProgress(progress, startDir)
        else:
            return super(CurveTile, self).getWorldCoordFromProgress(progress, startDir)


    def isMouth(self,entryCoord):
        curveComponent = super().getEntryAndExitCoord()
        straightComponent = super(CurveTile,self).getEntryAndExitCoord()

        mouth = False
        for i in curveComponent:
            if i in straightComponent:
                if i == entryCoord:
                    mouth = True
        return mouth

    def getEntryAndExitCoord(self, entryDir=None, currentStatus = False,diverge = None): #Entry dir is what is the part of the point to enter
        curveComponent = super().getEntryAndExitCoord() #current status ==False is all exits of point, current status == true is only exits that correspond to the current diverge state
        straightComponent = super(CurveTile,self).getEntryAndExitCoord()

        if diverge==None:
            tempDiverge = self.diverge
        else:
            tempDiverge =diverge

        if currentStatus==True:
            if tempDiverge==True:
                return curveComponent
            elif tempDiverge==False:
                return straightComponent

        if currentStatus==False:
            mixedComponent =[]

            for item in curveComponent:
                if item not in mixedComponent:
                    mixedComponent.append(item)
            for item in straightComponent:
                if item not in mixedComponent:
                    mixedComponent.append(item)

            if entryDir==None:
                return mixedComponent
            
            if entryDir in curveComponent and entryDir in straightComponent:
                return mixedComponent
            if entryDir in curveComponent:
                return curveComponent
            if entryDir in straightComponent:
                return straightComponent

    def getNextTileAdd(self, startDir):
        if self.diverge:
            return super().getNextTileAdd(startDir)
        else:
            return super(CurveTile, self).getNextTileAdd(startDir)


class PortalTile(TrackTile):
    def __init__(self, map_draw, imagePath, point, flip,location,tileCoord,distance, tilemap, connect ,clickable=False):
        super().__init__(map_draw, imagePath, point,flip ,location,tileCoord,distance, clickable)
        self.tilemap = tilemap
        self.connect = connect



    def getNextTileAdd(self, startDir):
        nextStartDir = (0,0)
        teleport = False

        if self.point =="east":
            nextStartDir= (0,-1)
            if startDir==(0,1):
                return nextStartDir
        elif self.point =="west":
            nextStartDir= (0,1)
            if startDir==(0,-1):
                return nextStartDir
        elif self.point =="south":
            nextStartDir= (-1,0)
            if startDir==(1,0):
                return nextStartDir
        elif self.point =="north" :
            nextStartDir= (1,0)
            if startDir==(-1,0):
                return nextStartDir
            
        
        #WE go to the portal tile
        for row in range(len(self.tilemap)):
            for column in range(len(self.tilemap[row])):
                tile = self.tilemap[row][column]
                if isinstance(tile,PortalTile):
                    if tile.connect == self.connect:
                        if self.tileLoc != tile.tileLoc:
                            return ("tele",tile.getDefaultStartDir(),(row,column))
        return (0,0)
