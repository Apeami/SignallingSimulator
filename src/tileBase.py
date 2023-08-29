import pyglet
import random

class TileBase:
    def __init__(self, openGlInstance, batch, imagePath, point,flip ,location, clickable=False):
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
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,distance, clickable=False,dimension = 50):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location, clickable)
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
        elif startDir == (1,1):
            self.startCoord = (self.location[0]- self.dimension/2, self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0]+ self.dimension/2, self.location[1] + self.dimension/2)
        elif startDir == (-1,-1):
            self.startCoord = (self.location[0]+ self.dimension/2, self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0]- self.dimension/2, self.location[1] - self.dimension/2)
        elif startDir == (1,-1):
            self.startCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)
        elif startDir == (-1,1):
            self.startCoord = (self.location[0]+ self.dimension/2, self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0]- self.dimension/2, self.location[1] + self.dimension/2)


        current_x = self.startCoord[0] + (self.endCoord[0] - self.startCoord[0]) * progress
        current_y = self.startCoord[1] + (self.endCoord[1] - self.startCoord[1]) * progress
        return (current_x, current_y)

    
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
        if startDir == (0,1):
            return (0,-1)
        elif startDir == (0,-1):
            return (0,1)
        elif startDir == (1,0):
            return (-1,0)
        elif startDir == (-1,0):
            return (1,0)
        



class SignalTile(TrackTile):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location, clickable=False, signal="Red"):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,100, clickable)
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
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location,distance, clickable=False):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,distance, clickable)
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

        print("PROGRESS CURVE")
        print(EntryA)
        print(EntryB)

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
        self.startCoord = (self.location[0] +(entry[1]*self.dimension/2), self.location[0] +(entry[0]*self.dimension/2))
        self.endCoord = (self.location[0] +(exit[1]*self.dimension/2), self.location[0] +(exit[0]*self.dimension/2))

        current_x = self.startCoord[0] + (self.endCoord[0] - self.startCoord[0]) * progress
        current_y = self.startCoord[1] + (self.endCoord[1] - self.startCoord[1]) * progress
        return (current_x, current_y)
    
    def getNextTileAdd(self, startDir):
        return self.exit

class PointTile(CurveTile):
    def __init__(self, openGlInstance,batch, imagePath, point, flip,location, clickable=False, diverge=False):
        super().__init__(openGlInstance,batch, imagePath, point,flip ,location,50, clickable)
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
        # self.point
        # self.flip
        # startDir
        # self.diverge

        self.startCoord = (self.location[0] -(startDir[1]*self.dimension/2), self.location[0] -(startDir[0]*self.dimension/2))

        endDir = (0,0)

        if self.diverge ==False:
            endDir = startDir

        # if self.point =="east":
        #     if self.flip ==True:
        #         if self.startDir ==(0,1):
        #             if self.diverge:
        #                 endDir = (0,1)
        #             else:
        #                 endDir = (-1,1)
        #         if self.startDir == (0,-1) and self.diverge:
        #             endDir = (0,-1)



    def getNextTileAdd(self, startDir):
        pass

