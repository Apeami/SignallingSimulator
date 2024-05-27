import json

from train import Train

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from datetime import datetime, timedelta
from extra import *

class Timetable:
    def __init__(self,map_draw,ui,tileMapper):
        self.map_draw=map_draw
        self.ui = ui
        self.trainList = []
        self.selectedTrainIndex = None
        self.tileMapper = tileMapper

        self.headcodeLabel = self.ui.CurrentHeadcode
        self.trainTimetable = self.ui.TrainTimetable
        self.trainListTable = self.ui.TrainList

        self.selectedTrain = None
        self.end = False


    def updateClock(self, time):

        # if self.selectedTrainIndex!=None:
        #     self.updateTrainInformation(time)

        self.updateTrainList()

        for train in self.trainList:
            if train.deleted == True:
                self.trainList.remove(train)
                self.updateTrainList()

        if time == self.endTime:
            print("Simulation Ended")
            WarningBox("The simulation has ended because the alloted time has passed", "Info").exec_()
            self.end = True
            return False
        if self.end==False:
            for train in self.trainData:
                if self.time_to_seconds(train['LoadTime']) == time:
                    #load the train in
                    for event in train['Schedule']:
                        event['Time'] = self.time_to_seconds(event['Time'])
                    self.trainList.append(Train(train,self.map_draw,self.tileMapper,self))
                    self.updateTrainList()

            for activeTrain in self.trainList:
                activeTrain.updateEvent(time)
        return True

    def openFile(self,fileName):
        #Read from the json file
        timetableData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.
        self.map_name = timetableData["MapName"]
        
        self.trainData = timetableData["Trains"]

        self.startTime = self.time_to_seconds(timetableData['StartTime'])
        self.endTime = self.time_to_seconds(timetableData['EndTime'])

    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data
    
    def updateTrainList(self):
        self.trainListTable.setRowCount(len(self.trainList))

        sorted_trains = sorted(self.trainList, key=lambda train: train.nextWaypointTime)

        rowNum = 0
        for train in sorted_trains:
            self.trainListTable.setItem(rowNum, 0, QTableWidgetItem(train.headcode)) #Headcode
            self.trainListTable.setItem(rowNum, 1, QTableWidgetItem(self.secondsToTime(train.nextWaypointTime))) #Time of next arrival
            self.trainListTable.setItem(rowNum, 2, QTableWidgetItem(train.nextWaypointName)) #Next Station

            self.trainListTable.setItem(rowNum, 3, QTableWidgetItem(train.destination)) #FinalDestination
            self.trainListTable.setItem(rowNum, 4, QTableWidgetItem(train.sorted_schedule[-1]['Location'])) #End Section
            self.trainListTable.setItem(rowNum, 5, QTableWidgetItem(""))

            for col in range(self.trainListTable.columnCount()):
                cell_item = self.trainListTable.item(rowNum, col)
                if cell_item is not None:
                    cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            if train == self.selectedTrain:
                for col in range(self.trainListTable.columnCount()):
                    cell_item = self.trainListTable.item(rowNum, col)
                    if cell_item is not None:
                        cell_item.setForeground(QColor(255, 0, 0))

            rowNum = rowNum + 1

        self.trainListTable.resizeColumnsToContents()

    def updateTrainInformation(self):
        train  = self.trainList[self.selectedTrainIndex]

        self.headcodeLabel.setText("Headcode: "+ train.headcode)

        self.trainTimetable.setRowCount(len(train.sorted_schedule))  # Number of rows

        for row, item in enumerate(train.sorted_schedule):
            # if item['Time']< time:
            #     for col in range(4):
            #         highlighted_item = self.trainTimetable.item(row, col)  # Assuming you want to highlight the first cell of the row
            #         highlighted_item.setBackground(Qt.red)
            self.trainTimetable.setItem(row, 0, QTableWidgetItem(self.secondsToTime(item['Time']))) #Time
            self.trainTimetable.setItem(row, 1, QTableWidgetItem(item['Action'])) #Action

            self.trainTimetable.setItem(row, 2, QTableWidgetItem(item['Location'])) #Location
            self.trainTimetable.setItem(row, 3, QTableWidgetItem("")) #Center


            for col in range(self.trainTimetable.columnCount()):
                cell_item = self.trainTimetable.item(row, col)
                if cell_item is not None:
                    cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            # for col, value in enumerate(item.values()):
            #     cell_item = QTableWidgetItem(str(value))
            #     cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            #     self.trainTimetable.setItem(row, col, cell_item)

        self.trainTimetable.resizeColumnsToContents()
        self.updateTrainList()

    def canvasMousePressEvent(self, mapX,mapY):
        index = 0
        for train in self.trainList:
            if mapX>train.trainCoord[0] and mapX<train.trainCoord[0]+train.width and mapY>train.trainCoord[1]-train.height and mapY<train.trainCoord[1]:
                self.selectedTrainIndex = index
                self.selectedTrain = self.trainList[self.selectedTrainIndex]
                self.updateTrainInformation()
            index = index + 1

    def delete(self):
        self.map_draw.train_list = {}
        #self.openGlInstance.removeBatch("trainList")

    def time_to_seconds(self,time_str):
        time_format = "%H:%M:%S"
        midnight = datetime.strptime("00:00:00", time_format)
        time = datetime.strptime(time_str, time_format)
        seconds_past_midnight = (time - midnight).seconds
        return seconds_past_midnight
    
    def secondsToTime(self,startTime):
        second = startTime
        hour = second // 3600
        second %= 3600
        minute = second // 60
        second %= 60
        return f"{hour:02}:{minute:02}:{second:02}"
