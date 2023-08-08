import pyglet

class Train:
    def __init__(self,trainData,openGlInstance,shape,headcode):
        self.openGlInstance = openGlInstance
        self.shape = shape
        self.headcode = headcode

        #self.headcode = trainData['Headcode']
        #self.maxSpeed = trainData['MaxSpeed']

        #self.sorted_schedule = sorted(trainData["Schedule"], key=lambda x: x["Time"])

        self.currentEvent = 0

    def updateMajorEvent(self):
        pass

    def updateMinorEvent(self):
        pass

    def drawTrain(self,worldPos):

        width, height = 40, 20
        x = worldPos[0]+25 -(width/2)
        y = worldPos[1]+25 -(height/2)

        rectLayer = pyglet.graphics.OrderedGroup(2)
        textLayer = pyglet.graphics.OrderedGroup(3)

        # Draw text on the rectangle
        label = pyglet.text.Label(self.headcode,
            font_name='Arial',
            font_size=12,
            x=x + width/2, y=y + height/2,
            anchor_x='center', anchor_y='center',
            batch=self.openGlInstance.batch,
            group = textLayer
        )

        rectangle_vertices = (x, y, x + width, y, x + width, y + height, x, y + height)
        rectangle_colors = (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
        self.openGlInstance.batch.add(4, pyglet.gl.GL_QUADS,rectLayer,
              ('v2f', rectangle_vertices),
              ('c3B', rectangle_colors))

