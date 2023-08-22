import json

from train import Train

class Timetable:
    def __init__(self,openGlInstance,shape):
        self.openGlInstance=openGlInstance
        self.shape = shape
        self.trainList = []

    def openFile(self,fileName):
        #Read from the json file
        timetableData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.
        self.map_name = timetableData["MapName"]
        self.simTime = timetableData["SimTime"]
        
        trainData = timetableData["Trains"]

        for train in trainData:
            pass

        
        self.trainList.append(Train(",.u",self.openGlInstance,self.shape,"9K94"))
        self.trainList[0].drawTrain((50,50))

    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data
    
    def canvasMousePressEvent(self, x,y,left,right,top,bottom,width,height):
        propX = x/width
        propY = y/height

        mapX = left + propX * (right-left)
        mapY = top + propY * (bottom-top)

        print("Start")
        print(mapX)
        print(mapY)
        

        for train in self.trainList:
            print(train.trainCoord)
            print(train.width)
            print(train.height)
            if mapX>train.trainCoord[0] and mapX<train.trainCoord[0]+train.width and mapY>train.trainCoord[1] and mapY<train.trainCoord[1]+train.height:
                print("Train Click")