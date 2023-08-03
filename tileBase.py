import pyglet
import random

class TileBase:
    def __init__(self, openGlInstance, imagePath, point, location, clickable=False):
        print("tilebase Create")
        print(openGlInstance.batch)
        image = pyglet.image.load(imagePath)

        self.width = image.width
        self.height = image.height

        self.point = point
        self.convert = {"north":270,"east":0,"south":90,"west":180}

        #image = image.get_texture().get_transform(rotate=self.convert[point])

        self.sprite = pyglet.sprite.Sprite(image, batch=openGlInstance.batch)

        self.sprite.anchor_x = self.width // 2
        self.sprite.anchor_y = self.height // 2

        if self.point=="west":
            self.sprite.update(location[0]+self.width, location[1]+self.height)
        if self.point=="east":
            self.sprite.update(location[0], location[1])
        if self.point=="north":
            self.sprite.update(location[0], location[1]+self.height)
        if self.point=="south":
            self.sprite.update(location[0]+self.width, location[1])
        self.sprite.rotation = self.convert[point]

        openGlInstance.shapes.append(self.sprite)

        self.clickable=clickable
        self.location = location
        self.openGlInstance = openGlInstance

        self.highlighted = False
        self.highlight = None



    def remove_from_batch(self):
        self.sprite.delete()

    def handleClick(self):
        print("Clicked")

        if self.highlighted==True:
            self.handleClickOff()
        else:
            image = pyglet.image.load("Assets/select.png")
            self.highlight = pyglet.sprite.Sprite(image, batch=self.openGlInstance.batch)
            self.highlight.update(self.location[0], self.location[1])
            self.openGlInstance.shapes.append(self.highlight)
            self.highlighted=True

    def handleClickOff(self):
        print("Clickoff")
        if self.highlight != None:
            self.highlight.delete()
            self.highlighted = False
            self.highlight=None


class SignalTile(TileBase):
    def __init__(self, openGlInstance, imagePath, point, location, clickable=False, signal="Red"):
        super().__init__(openGlInstance, imagePath, point, location, clickable)
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
        #new_image = new_image.get_texture().get_transform(rotate=self.convert[self.point])

        self.sprite.image = new_image