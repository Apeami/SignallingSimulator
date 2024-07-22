
from tileBase import *
import queue
import asyncio
from extra import WarningBox

class Train:
    def __init__(self,trainData,map_draw,tileMapper,timetable):
        self.map_draw = map_draw
        self.trainCoord = [0,0]
        self.tileMapper = tileMapper
        self.timetable = timetable

        self.headcode = trainData['Headcode']
        self.maxSpeed = trainData['MaxSpeed']
        self.destination = trainData['Destination']

        self.sorted_schedule = sorted(trainData["Schedule"], key=lambda x: x["Time"])

        self.nextWaypointName = self.sorted_schedule[0]['Location']
        self.nextWaypointAction = self.sorted_schedule[0]['Action']
        self.nextWaypointTime = self.sorted_schedule[0]['Time']
        self.prevWaypointName = None

        self.currentEvent = 0
        self.currentDisplayEvent = 0

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

        self.trainReadyTime = 0
        self.trainStopped = False

        self.prevSignalTile = None

        self.canDespawn = False
        self.despawnTileName = None

        self.deleted = False

    def updateEvent(self,time):
        self.time = time


        self.manageRestartSignal()
        self.manageRestartStop()
        


        if self.currentEvent == 0:
            event = self.sorted_schedule[self.currentEvent]
            if event['Time'] == time and event['Action'] =='Spawn':
                    self.spawnTrain(event['Location'])
                    self.currentEvent = self.currentEvent + 1
                    self.currentDisplayEvent = self.currentEvent
                    self.timetable.updateTrainList()

                    if len(self.sorted_schedule)>self.currentEvent:
                        self.prevWaypointName = self.nextWaypointName
                        self.nextWaypointName = self.sorted_schedule[self.currentEvent]['Location']
                        self.nextWaypointAction =self.sorted_schedule[self.currentEvent]['Action']
                        self.nextWaypointTime = self.sorted_schedule[self.currentEvent]['Time']



        if self.exist:
            self.manageAction()
            self.reDrawTrain(self.getNextPosition(self.currentSpeed,0.000277))



    def manageRestartSignal(self):
        if isinstance(self.tileObjNext, SignalTile) and self.tileObjNext.signal!="Red":
            self.currentSpeed = self.maxSpeed
            self.tileObjNext.trainPassed()
            self.tileObjNext.trainInBlock = True
            if self.prevSignalTile!=None:
                self.prevSignalTile.trainInBlock=False
            self.tileMapper.updateSignals()
            self.prevSignalTile = self.tileObjNext


    def manageRestartStop(self):
        if self.trainStopped and self.trainReadyTime<=self.time:
            self.currentSpeed = self.maxSpeed
            self.trainStopped = False
            self.currentDisplayEvent = self.currentEvent
            self.timetable.updateTrainList()


    def manageNewTile(self):
        if isinstance(self.tileObjNext, SignalTile):
            if self.tileObjNext.getDefaultStartDir()==(-self.entryToTile[0],-self.entryToTile[1]): #If signal in same direction
                if self.tileObjNext.signal=="Red":
                    self.currentSpeed = 0
                    self.tileProgress = 0.5
                else:
                    self.tileObjNext.trainPassed()
                    self.tileObjNext.trainInBlock = True
                    if self.prevSignalTile!=None:
                        self.prevSignalTile.trainInBlock=False
                    self.tileMapper.updateSignals()
                    self.prevSignalTile = self.tileObjNext
                

    def manageAction(self):
        if self.currentTileName == self.nextWaypointName:#The train has arrived at the certain waypoint
            if self.nextWaypointAction =="Call":
                self.currentSpeed = 0
                self.tileProgress = 0.5

                waitTime = 10
                if self.time<self.nextWaypointTime- waitTime:
                    self.trainReadyTime = self.nextWaypointTime
                else: 
                    self.trainReadyTime = self.time + waitTime

                self.trainStopped = True
            
            if self.nextWaypointAction =="Despawn":
                self.deleteTrain()
                if self.prevSignalTile!=None:
                    self.prevSignalTile.trainInBlock=False
                self.tileMapper.updateSignals()

            if self.nextWaypointAction == "Stop":
                self.currentSpeed = 0
                self.tileProgress = 0.5

            if self.nextWaypointAction =="Start":
                if self.time<self.nextWaypointTime:
                    self.trainReadyTime = self.nextWaypointTime
                else: 
                    self.trainReadyTime = self.time + 1
                self.trainStopped=True

            if self.nextWaypointAction =="Reverse":
                self.entryToTile = [-self.entryToTilePrev[0],-self.entryToTilePrev[1]]
                self.entryToTilePrev = [-self.entryToTile[0],-self.entryToTile[1]]

            if self.nextWaypointAction!="Despawn" or self.nextWaypointAction!="Call" or self.nextWaypointAction!="Start":
                self.currentDisplayEvent = self.currentDisplayEvent +1

            if self.nextWaypointAction!="Despawn":
                self.currentEvent = self.currentEvent + 1


            
            self.timetable.updateTrainList()

            if len(self.sorted_schedule)>self.currentEvent:
                self.prevWaypointName = self.nextWaypointName
                self.nextWaypointName = self.sorted_schedule[self.currentEvent]['Location']
                self.nextWaypointAction =self.sorted_schedule[self.currentEvent]['Action']
                self.nextWaypointTime = self.sorted_schedule[self.currentEvent]['Time']

        #New feature
        # elif self.currentTileName != self.nextWaypointName and self.currentTileName!=None and self.currentTileName!=self.prevWaypointName:
        #     self.deleteTrain() 
        #     print("TRAIN AT WRONG WAYPOINT")
        #     print(self.currentTileName)
        #     print(self.nextWaypointName)
        #     WarningBox(self.headcode + " may have arrived at the wrong waypoint.","Cannot complete").exec_()
            

    def getNextPosition(self,speed,timeIncrease):
        realDistanceIncrease = speed * timeIncrease
        progressInclease = realDistanceIncrease / (self.tileObj.distance/1000)
        self.tileProgress = self.tileProgress +progressInclease 

        # if isinstance(self.tileObj, SignalTile) and self.tileObj.signal=="Red":
        #         self.tileProgress=0        

        if self.tileProgress>0.5 and not self.tileIncreased: #Get Next Tile Obj
            self.tileIncreased = True
            nextTileAdder = self.tileObj.getNextTileAdd(self.entryToTile)
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
                

            self.tileProgress = tileProgressRemainder * (self.prevDistance / self.tileObj.distance)

            self.prevDistance = self.tileObj.distance


        return self.tileObj.getWorldCoordFromProgress(self.tileProgress,self.entryToTilePrev)

    def spawnTrain(self,spawnName):
        
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

        self.exist=True
        self.currentSpeed = self.maxSpeed


    def deleteTrain(self):
        if self.deleted == False:
            self.map_draw.del_train(self.headcode)
            self.deleted = True

    def reDrawTrain(self, worldPos):
        x = worldPos[0] + 25 - (self.width / 2)
        y = worldPos[1] - 25 + (self.height / 2)

        self.trainCoord = [x, y]

        self.map_draw.draw_train(self.trainCoord, self.headcode)

        # # Update the label's position
        # self.label.x = x + self.width / 2
        # self.label.y = y + self.height / 2

        # # Update the rectangle's vertices
        # rectangle_vertices = (x, y, x + self.width, y, x + self.width, y + self.height, x, y + self.height)
        # self.rectangle.vertices = rectangle_vertices

    def drawTrain(self,worldPos):

        x = worldPos[0]
        y = worldPos[1]

        self.trainCoord = [x,y]

        self.map_draw.draw_train(self.trainCoord, self.headcode)

        # rectLayer = pyglet.graphics.OrderedGroup(2)
        # textLayer = pyglet.graphics.OrderedGroup(3)

        # # Draw text on the rectangle
        # self.label = pyglet.text.Label(self.headcode,
        #     font_name='Arial',
        #     font_size=12,
        #     x=x + self.width/2, y=y + self.height/2,
        #     anchor_x='center', anchor_y='center',
        #     batch=self.batch,
        #     group = textLayer
        # )

        # rectangle_vertices = (x, y, x + self.width, y, x + self.width, y + self.height, x, y + self.height)
        # rectangle_colors = (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
        # self.rectangle = self.batch.add(4, pyglet.gl.GL_QUADS,rectLayer,
        #       ('v2f', rectangle_vertices),
        #       ('c3B', rectangle_colors))
    


