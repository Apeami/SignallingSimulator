import pyglet
import random

class TileBase:
    def __init__(self, openGlInstance, imagePath, flipX,flipY,vertical, location):
        print("tilebase Create")
        print(openGlInstance.batch)
        image = pyglet.image.load(imagePath)

        if flipX:
            image = image.get_texture().get_transform(flip_x=True)
        if flipY:
            image = image.get_texture().get_transform(flip_y=True)
        if vertical:
            image = image.get_texture().get_transform(rotate=90)

        sprite = pyglet.sprite.Sprite(image, batch=openGlInstance.batch)

        sprite.update(location[0], location[1])

        openGlInstance.shapes.append(sprite)


    def remove_from_batch(self):
        self.sprite.delete()