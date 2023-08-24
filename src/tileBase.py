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
            self.sprite.update(locationEdited[0], locationEdited[1]+self.height)
        if self.point=="south":
            self.sprite.update(locationEdited[0]+self.width, locationEdited[1])

        self.sprite.rotation = self.convert[point]


        self.openGlInstance.shapes.append(self.sprite)

        

    def remove_from_batch(self):
        self.sprite.delete()

    def handleClick(self):
        print("Clicked")

        if self.highlighted==True:
            self.handleClickOff()
        else:
            image = pyglet.image.load("Assets/select.png")
            self.highlight = pyglet.sprite.Sprite(image, batch=self.batch)
            self.highlight.update(self.location[0], self.location[1])
            self.openGlInstance.shapes.append(self.highlight)
            self.highlighted=True

    def handleClickOff(self):
        print("Clickoff")
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

        if startDir == "east":
            self.startCoord = (self.location[0] - self.dimension/2, self.location[1])
            self.endCoord = (self.location[0] + self.dimension/2, self.location[1])
        elif startDir == "west":
            self.startCoord = (self.location[0] + self.dimension/2, self.location[1])
            self.endCoord = (self.location[0] - self.dimension/2, self.location[1])
        elif startDir == "north":
            self.startCoord = (self.location[0], self.location[1] + self.dimension/2)
            self.endCoord = (self.location[0], self.location[1] - self.dimension/2)
        elif startDir == "south":
            self.startCoord = (self.location[0], self.location[1] - self.dimension/2)
            self.endCoord = (self.location[0], self.location[1] + self.dimension/2)

        current_x = self.startCoord[0] + (self.endCoord[0] - self.startCoord[0]) * progress
        current_y = self.startCoord[1] + (self.endCoord[1] - self.startCoord[1]) * progress
        return (current_x, current_y)

    
    def getDefaultStartDir(self):
        if self.point =="east":
            return "west"
        if self.point =="west":
            return "east"
        if self.point =="north":
            return "south"
        if self.point =="north":
            return "south"
        
    def getNextTileAdd(self,startDir):
        if startDir == "east":
            return (0,1)
        elif startDir == "west":
            return (0,-1)
        elif startDir == "north":
            return (1,0)
        elif startDir == "south":
            return (-1,0)
        



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


class PointTile(TrackTile):
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