import pyglet
import random
import math

class TileBase:
    def __init__(self, openGlInstance, batch, imagePath, point,flip ,location,tileCoord,clickable=False):
        print("tilebase Create")

        #Image creation
        image = pyglet.image.load(imagePath)

        #Variable and constant creation
        self.width = image.width
        self.height = image.height
        self.point = point
        self.convert = {"north":270,"east":0,"south":90,"west":180}
        self.highlighted = False
        self.highlight=None
        self.openGlInstance = openGlInstance
        self.location = location
        self.flip=flip
        self.batch = batch
        self.tileCoord = tileCoord
        self.tileLoc = (math.floor(self.location[0]/50), math.floor(self.location[1]/50))

        #Sprite managment

        if self.flip:
            image = image.get_texture().get_transform(flip_y=True)  

        self.sprite = pyglet.sprite.Sprite(image, batch=self.batch)

        self.sprite.anchor_x = self.width // 2
        self.sprite.anchor_y = self.height // 2

        locationEdited = [self.location[0],self.location[1]]
        if self.width>50:
            locationEdited[0] = locationEdited[0] - ((self.width-50)/2)
        if self.height>50:
            locationEdited[1] = locationEdited[1] - ((self.height-50)/2)

            
        if self.point=="west":
            if self.flip:
                locationEdited[1]=locationEdited[1]-self.height
            self.sprite.update(locationEdited[0]+self.width, locationEdited[1]+self.height)
        if self.point=="east":
            if self.flip:
                locationEdited[1]=locationEdited[1]+self.height
            self.sprite.update(locationEdited[0], locationEdited[1])
        if self.point=="north":
            if self.flip:
                locationEdited[0]=locationEdited[0]-self.width
            self.sprite.update(locationEdited[0]+self.width, locationEdited[1])
        if self.point=="south":
            if self.flip:
                locationEdited[0]=locationEdited[0]+self.width
            self.sprite.update(locationEdited[0], locationEdited[1]+self.height)

        self.sprite.rotation = self.convert[point]


        self.openGlInstance.shapes.append(self.sprite)

        

    def remove_from_batch(self):
        self.sprite.delete()

    def handleClick(self):

        if self.highlighted==True:
            self.handleClickOff()
        else:
            image = pyglet.image.load("Assets/select.png")
            self.highlight = pyglet.sprite.Sprite(image, batch=self.batch)
            self.highlight.update(self.location[0], self.location[1])
            self.openGlInstance.shapes.append(self.highlight)
            self.highlighted=True

    def handleClickOff(self):
        if self.highlight != None:
            self.highlight.delete()
            self.highlighted = False
            self.highlight=None


class TrackTile(TileBase):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,tileCoord,distance, clickable=False,dimension = 50):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,tileCoord, clickable)
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
            self.startCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)
        elif startDir == (1,-1):
            self.startCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)


        current_x = self.startCoord[0] + (self.endCoord[0] - self.startCoord[0]) * progress
        current_y = self.startCoord[1] + (self.endCoord[1] - self.startCoord[1]) * progress
        return (current_x, current_y)

    def getEntryAndExitCoord(self):
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
        



class SignalTile(TrackTile):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,tileCoord, clickable=False, signal="Red"):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,tileCoord,100, clickable)
        self.signal = signal

    def setSignal(self,signal):
        self.signal = signal

        if signal == "Green":
            newImagePath = "Assets/trackGreenSignal.png"
        elif signal == "DYellow":
            newImagePath = "Assets/trackDYellowSignal.png"
        elif signal == "Yellow":
            newImagePath = "Assets/trackYellowSignal.png"
        elif signal == "Red":
            newImagePath = "Assets/trackRedSignal.png"
        else:
            newImagePath = "Assets/trackRedSignal.png"

        new_image = pyglet.image.load(newImagePath)

        if self.flip:
            new_image = new_image.get_texture().get_transform(flip_y=True)  

        self.sprite.image = new_image


class CurveTile(TrackTile):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,distance,tileCoord, clickable=False):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,distance,tileCoord, clickable)
        self.exit = None

    def getEntryAndExitCoord(self):
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

        EntryA, EntryB = self.getEntryAndExitCoord()

        if EntryA == startDir:
            exit = EntryB
            entry = EntryA
        elif EntryB == startDir:
            exit = EntryA 
            entry = EntryB
        else:
            print("No matching entry")
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
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,tileCoord, clickable=False, diverge=False):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,tileCoord,50, clickable)
        self.diverge=diverge

    def togglePoint(self):

        if self.diverge:
            self.diverge = False
            newImagePath = "Assets/pointStraight.png"
        else:
            self.diverge = True
            newImagePath = "Assets/pointCurve.png"

        new_image = pyglet.image.load(newImagePath)

        if self.flip:
            new_image = new_image.get_texture().get_transform(flip_y=True)  

        self.sprite.image = new_image

    def getWorldCoordFromProgress(self, progress, startDir):
        if self.diverge:
            return super().getWorldCoordFromProgress(progress, startDir)
        else:
            return super(CurveTile, self).getWorldCoordFromProgress(progress, startDir)


    def getEntryAndExitCoord(self):
        curveComponent = super().getEntryAndExitCoord()
        straightComponent = super(CurveTile,self).getEntryAndExitCoord()

        finalComponent =[]

        for item in curveComponent:
            if item not in finalComponent:
                finalComponent.append(item)
        for item in straightComponent:
            if item not in finalComponent:
                finalComponent.append(item)

    def getNextTileAdd(self, startDir):
        if self.diverge:
            return super().getNextTileAdd(startDir)
        else:
            return super(CurveTile, self).getNextTileAdd(startDir)


class PortalTile(TrackTile):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,tileCoord,distance, tilemap, connect ,clickable=False):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,tileCoord,distance, clickable)
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
                    print("TILE CONNECT")
                    print(tile.connect)
                    print(self.connect)
                    if tile.connect == self.connect:
                        print("POSSIBLE MATCH")
                        print((row,column))
                        print(self.tileLoc)
                        print(tile.tileLoc)
                        if self.tileLoc != tile.tileLoc:
                            return ("tele",tile.getDefaultStartDir(),(row,column))
        return (0,0)