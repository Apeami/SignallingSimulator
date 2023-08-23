import json

from train import Train

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

class Timetable:
    def __init__(self,openGlInstance,shape,ui):
        self.openGlInstance=openGlInstance
        self.shape = shape
        self.ui = ui
        self.trainList = []
        self.selectedTrainIndex = None

        self.headcodeLabel = self.ui.CurrentHeadcode
        self.trainTimetable = self.ui.TrainTimetable
        self.trainListTable = self.ui.TrainList

        self.trainBatch = self.openGlInstance.createNewBatch("trainList")

    def openFile(self,fileName):
        #Read from the json file
        timetableData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.
        self.map_name = timetableData["MapName"]
        self.simTime = timetableData["SimTime"]
        
        trainData = timetableData["Trains"]

        for train in trainData:
            self.trainList.append(Train(train,self.trainBatch,self.shape))

        
        self.trainList[0].drawTrain((50,50))
        self.trainList[1].drawTrain((150,50))

        self.updateTrainList()

    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data
    
    def updateTrainList(self):
        self.trainListTable.setRowCount(len(self.trainList))

        rowNum = 0
        for train in self.trainList:
            self.trainListTable.setItem(rowNum, 0, QTableWidgetItem(train.headcode)) #Headcode
            self.trainListTable.setItem(rowNum, 1, QTableWidgetItem(train.sorted_schedule[train.currentEvent]['Location'])) #Next Station
            self.trainListTable.setItem(rowNum, 2, QTableWidgetItem(str(train.sorted_schedule[train.currentEvent]['Time']))) #Time of next arrival
            self.trainListTable.setItem(rowNum, 3, QTableWidgetItem(train.destination)) #FinalDestination
            self.trainListTable.setItem(rowNum, 4, QTableWidgetItem(train.sorted_schedule[-1]['Location'])) #End Section
            self.trainListTable.setItem(rowNum, 5, QTableWidgetItem(""))

            for col in range(self.trainListTable.columnCount()):
                cell_item = self.trainListTable.item(rowNum, col)
                if cell_item is not None:
                    cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            rowNum = rowNum + 1

        self.trainListTable.resizeColumnsToContents()

    def updateTrainInformation(self):
        train  = self.trainList[self.selectedTrainIndex]

        self.headcodeLabel.setText("Headcode: "+ train.headcode)

        self.trainTimetable.setRowCount(len(train.sorted_schedule))  # Number of rows

        for row, item in enumerate(train.sorted_schedule):
            for col, value in enumerate(item.values()):
                cell_item = QTableWidgetItem(str(value))
                cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.trainTimetable.setItem(row, col, cell_item)

        self.trainTimetable.resizeColumnsToContents()

    def canvasMousePressEvent(self, x,y,left,right,top,bottom,width,height):
        propX = x/width
        propY = y/height

        mapX = left + propX * (right-left)
        mapY = top + propY * (bottom-top)

        
        index = 0
        for train in self.trainList:
            if mapX>train.trainCoord[0] and mapX<train.trainCoord[0]+train.width and mapY>train.trainCoord[1] and mapY<train.trainCoord[1]+train.height:
                self.selectedTrainIndex = index
                self.updateTrainInformation()
            index = index + 1

    def delete(self):
        self.openGlInstance.removeBatch("trainList")