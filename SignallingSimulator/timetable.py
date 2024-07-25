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

    def checkForTrainInTile(self, trainCheck):
        for train in self.trainList:
            if train.tileObj == trainCheck.tileObj and train!=trainCheck:
                return True
        return False

    def updateTrainInformation(self):
        if self.selectedTrainIndex!=None:
            train  = self.trainList[self.selectedTrainIndex]

            self.headcodeLabel.setText("Headcode: "+ train.headcode)

            self.trainTimetable.setRowCount(len(train.sorted_schedule))  # Number of rows

            for row, item in enumerate(train.sorted_schedule):
                # Determine if this row is before the current event
                if row < train.currentEvent:
                    time_text = f"<s>{self.secondsToTime(item['Time'])}</s>"
                    action_text = f"<s>{item['Action']}</s>"
                    location_text = f"<s>{item['Location']}</s>"
                else:
                    time_text = self.secondsToTime(item['Time'])
                    action_text = item['Action']
                    location_text = item['Location']

                #Set temp value of location item for enabling teleporting
                # dataItem = QTableWidgetItem(item['Location'])#.setForeground(QColor(255, 255, 255, 0))
                # self.trainTimetable.setItem(row, 2, dataItem) #Location


                # Create QLabel to render HTML content
                time_label = QLabel(time_text)
                time_label.setTextFormat(Qt.RichText)
                time_label.setAlignment(Qt.AlignCenter)
                self.trainTimetable.setCellWidget(row, 0, time_label)

                action_label = QLabel(action_text)
                action_label.setTextFormat(Qt.RichText)
                action_label.setAlignment(Qt.AlignCenter)
                self.trainTimetable.setCellWidget(row, 1, action_label)

                location_label = QLabel(location_text)
                location_label.setTextFormat(Qt.RichText)
                location_label.setAlignment(Qt.AlignCenter)
                self.trainTimetable.setCellWidget(row, 2, location_label)

                # Empty cell in the 4th column
                empty_label = QLabel("")
                self.trainTimetable.setCellWidget(row, 3, empty_label)

                for col in range(self.trainTimetable.columnCount()):
                    cell_item = self.trainTimetable.item(row, col)
                    if cell_item is not None:
                        cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

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
        print("DELTING")
        # for train in self.trainList:
        #     train.deleteTrain()
        self.trainList = []
        self.map_draw.train_list = {}
        self.map_draw.update()
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

    def zoomtoselectedtrain(self):
        if self.selectedTrainIndex!=None:
            train  = self.trainList[self.selectedTrainIndex]
            self.zoomtotrain(train.headcode)

    def zoomtotrain(self,headcode):
        print("Zooming to ")
        print(headcode)
        for train in self.trainList:
            if train.headcode == headcode:
                self.selectedTrainIndex = self.trainList.index(train)
                self.updateTrainInformation()
                if train.exist:
                    self.map_draw.zoomToPoint(train.trainCoord)
                else: #Train don't exist
                    print("NOT exist")
                    print(train.nextWaypointName)
                    self.tileMapper.zoomtopoint(train.nextWaypointName)
