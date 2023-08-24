import pyglet

class Train:
    def __init__(self,trainData,batch,shape,tileMapper):
        self.batch = batch
        self.shape = shape
        self.trainCoord = [0,0]
        self.tileMapper = tileMapper

        self.headcode = trainData['Headcode']
        self.maxSpeed = trainData['MaxSpeed']
        self.destination = trainData['Destination']

        self.sorted_schedule = sorted(trainData["Schedule"], key=lambda x: x["Time"])

        self.currentEvent = 0

        self.width, self.height = 40, 20

        self.exist = False
        

    def updateEvent(self,time):


        event = self.sorted_schedule[self.currentEvent]
        if event['Time'] == time:
            print("Train event")
            print(self.headcode)
            print(event['Action'])

            if event['Action'] =='Spawn':
                spawnName = event['Location']
                coord = self.tileMapper.getCoordFromName(spawnName)
                self.tileProgress = 0
                self.tileObj = self.tileMapper.tileMap[coord[0]][coord[1]]
                self.entryToTile = self.tileObj.getDefaultStartDir()
                worldCoord = self.tileObj.getWorldCoordFromProgress(self.tileProgress,self.entryToTile)
                self.drawTrain(worldCoord)
                self.exist=True
            if self.currentEvent<len(self.sorted_schedule)-1:
                self.currentEvent = self.currentEvent + 1

        if self.exist:
            self.reDrawTrain(self.getNextPosition(self.maxSpeed,0.000277))

    def getNextPosition(self,speed,timeIncrease):
        print(self.tileObj.distance)
        realDistanceIncrease = speed * timeIncrease
        progressInclease = realDistanceIncrease / (self.tileObj.distance/1000)
        self.tileProgress = self.tileProgress +progressInclease 
        return self.tileObj.getWorldCoordFromProgress(self.tileProgress,self.entryToTile)


    def reDrawTrain(self, worldPos):
        x = worldPos[0] + 25 - (self.width / 2)
        y = worldPos[1] + 25 - (self.height / 2)

        self.trainCoord = [x, y]

        # Update the label's position
        self.label.x = x + self.width / 2
        self.label.y = y + self.height / 2

        # Update the rectangle's vertices
        rectangle_vertices = (x, y, x + self.width, y, x + self.width, y + self.height, x, y + self.height)
        self.rectangle.vertices = rectangle_vertices

    def drawTrain(self,worldPos):

        x = worldPos[0]+25 -(self.width/2)
        y = worldPos[1]+25 -(self.height/2)

        self.trainCoord = [x,y]

        rectLayer = pyglet.graphics.OrderedGroup(2)
        textLayer = pyglet.graphics.OrderedGroup(3)

        # Draw text on the rectangle
        self.label = pyglet.text.Label(self.headcode,
            font_name='Arial',
            font_size=12,
            x=x + self.width/2, y=y + self.height/2,
            anchor_x='center', anchor_y='center',
            batch=self.batch,
            group = textLayer
        )

        rectangle_vertices = (x, y, x + self.width, y, x + self.width, y + self.height, x, y + self.height)
        rectangle_colors = (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
        self.rectangle = self.batch.add(4, pyglet.gl.GL_QUADS,rectLayer,
              ('v2f', rectangle_vertices),
              ('c3B', rectangle_colors))
    


