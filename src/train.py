import pyglet
from tileBase import *
import queue
import asyncio

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
        self.currentTile = None

        self.prevDistance = None

        self.currentTileName = None

        self.currentSpeed = 0

        self.entryToTile = None
        self.entryToTilePrev = None

        self.tileObj = None
        self.tileObjNext = None

        self.tileIncreased = False

        self.stopEventBacklog = queue.Queue()

        self.trainReady = False
        self.trainReadyTime = 0
        self.trainStopped = False

        self.prevSignalTile = None

    def updateEvent(self,time):
        self.time = time

        if self.trainReadyTime == time:
            print("Getting TRAIN READY")
            self.trainReady = True

        self.manageRestartSignal()
        self.manageRestartStop()

        event = self.sorted_schedule[self.currentEvent]
        if event['Time'] == time:
            print("Train event")
            print(self.headcode)
            print(event['Action'])

            if event['Action'] =='Spawn':
                spawnName = event['Location']
                tempTile = self.tileMapper.getCoordFromName(spawnName)
                self.currentTile = [tempTile[0],tempTile[1]]
                self.tileProgress = 0
                self.tileObj = self.tileMapper.tileMap[self.currentTile[0]][self.currentTile[1]]
                self.entryToTile = self.tileObj.getDefaultStartDir()
                self.entryToTilePrev = self.entryToTile
                worldCoord = self.tileObj.getWorldCoordFromProgress(self.tileProgress,self.entryToTile)
                self.prevDistance = self.tileObj.distance
                self.drawTrain(worldCoord)
                self.currentTileName = self.tileMapper.getNameFromCoord(self.currentTile)
                if len(self.sorted_schedule)>self.currentEvent+1:
                    self.nextWaypointName = self.sorted_schedule[self.currentEvent+1]['Location']
                else:
                    print("No Stopping Waypoint")
                self.exist=True
                self.currentSpeed = self.maxSpeed

            if event['Action'] =="Stop":
                self.stopEventBacklog.put(event['Location'])


            if self.currentEvent<len(self.sorted_schedule)-1:
                self.currentEvent = self.currentEvent + 1


        if self.exist:
            self.reDrawTrain(self.getNextPosition(self.currentSpeed,0.000277))



    def manageRestartSignal(self):
        if isinstance(self.tileObjNext, SignalTile) and self.tileObjNext.signal!="Red":
            self.currentSpeed = self.maxSpeed
            self.tileObjNext.trainInBlock = True
            if self.prevSignalTile!=None:
                self.prevSignalTile.trainInBlock=False
            self.tileMapper.updateSignals()
            self.prevSignalTile = self.tileObjNext

    def manageRestartStop(self):
        if self.stopEventBacklog.qsize()>0 and self.trainReady:
            self.currentSpeed = self.maxSpeed
            self.trainReady = False
            self.nextWaypointName = self.sorted_schedule[self.currentEvent]['Location']


    def manageNewTile(self):
        if isinstance(self.tileObjNext, SignalTile):
            

            if self.tileObjNext.signal=="Red":
                self.currentSpeed = 0
                self.tileProgress = 0.5

            if self.tileObjNext.signal!="Red":
                self.tileObjNext.trainInBlock = True
                if self.prevSignalTile!=None:
                    self.prevSignalTile.trainInBlock=False
                self.tileMapper.updateSignals()
                self.prevSignalTile = self.tileObjNext
                

        if self.currentTileName == self.nextWaypointName:
            self.currentSpeed = 0
            self.tileProgress = 0.5
            self.trainReadyTime = self.time+10
            self.trainReady = False
            print("Action Stop")

            

    def getNextPosition(self,speed,timeIncrease):
        realDistanceIncrease = speed * timeIncrease
        progressInclease = realDistanceIncrease / (self.tileObj.distance/1000)
        self.tileProgress = self.tileProgress +progressInclease 

        # if isinstance(self.tileObj, SignalTile) and self.tileObj.signal=="Red":
        #         self.tileProgress=0        

        if self.tileProgress>0.5 and not self.tileIncreased: #Get Next Tile Obj
            self.tileIncreased = True
            nextTileAdder = self.tileObj.getNextTileAdd(self.entryToTile)
            print(nextTileAdder)
            if nextTileAdder[0]=="tele":#Teleport
                self.currentTile[0] = nextTileAdder[2][0]
                self.currentTile[1] = nextTileAdder[2][1]
                self.entryToTile = (nextTileAdder[1][0],nextTileAdder[1][1])
            else:
                self.currentTile[0] = self.currentTile[0] + nextTileAdder[0]
                self.currentTile[1] = self.currentTile[1] + nextTileAdder[1]
                self.entryToTile = (-nextTileAdder[0],-nextTileAdder[1])  


            self.tileObjNext = self.tileMapper.tileMap[self.currentTile[0]][self.currentTile[1]]
            
            self.manageNewTile()
        elif self.tileProgress>1: #Move to the next tile
            self.tileObj = self.tileObjNext
            self.currentTileName = self.tileMapper.getNameFromCoord(self.currentTile)
            self.tileIncreased=False
            self.entryToTilePrev = self.entryToTile


            tileProgressRemainder = self.tileProgress - 1
            #self.tileProgress = tileProgressRemainder
                
            print(tileProgressRemainder)
            print(self.prevDistance / self.tileObj.distance)
            self.tileProgress = tileProgressRemainder * (self.prevDistance / self.tileObj.distance)
            print(self.tileProgress)
            self.prevDistance = self.tileObj.distance


        return self.tileObj.getWorldCoordFromProgress(self.tileProgress,self.entryToTilePrev)


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
    


