import json

from train import Train

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox

from datetime import datetime, timedelta
from extra import *

import copy

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


    def updateClock(self, time, updatesPerSecond):

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
                print("Train Data")
                print(self.trainData)
                print("Train")
                print(train)
                print("LOAd time")
                print(train["LoadTime"])
                if self.time_to_seconds(train['LoadTime']) * updatesPerSecond == time:
                    #load the train in
                    print("Events")
                    for event in train['Schedule']:
                        print(event)
                        event['Time'] = self.time_to_seconds(event['Time'])
                    self.trainList.append(Train(train,self.map_draw,self.tileMapper,self))
                    self.updateTrainList()

            for activeTrain in self.trainList:
                activeTrain.updateEvent(time, updatesPerSecond)
        return True

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText("Error")
        error_dialog.setInformativeText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

    def openFile(self,fileName, tile_map_name):
        #Read from the json file
        timetableData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.

        if "type" not in timetableData or timetableData["type"]!= "timetable":
            self.show_error_message("File is not of type: timetable")
            return True

        if "name" not in timetableData:
            self.show_error_message("No map name provided")
            return True
        self.map_name = timetableData["name"]

        if self.map_name != tile_map_name:
            self.show_error_message("Timetable is not from the same map")
            return True
        
        if "Trains" not in timetableData:
            self.show_error_message("No train data provided")
            return True
        self.trainData = timetableData["Trains"]

        if "StartTime" not in timetableData or "EndTime" not in timetableData:
            self.show_error_message("No Start of EndTime provided")
            return True
        self.startTime = self.time_to_seconds(timetableData['StartTime'])
        self.endTime = self.time_to_seconds(timetableData['EndTime'])

        #Duplicate timetable data
        tempArray = []
        for train in timetableData["Trains"]:
            if "RepeatNum" in train and "RepeatInterval" in train:
                #This means we need to execute the duplication
                for i in range(train["RepeatNum"]):
                    newTrain = copy.deepcopy(train)
                    newTrain["LoadTime"] = self.secondsToTime(self.time_to_seconds(newTrain["LoadTime"])+((i+1)*self.time_to_seconds(train["RepeatInterval"])))

                    newTrain["Headcode"] = self.increment_with_mask(newTrain["Headcode"], newTrain["IncreaseHeadcode"], i+1 )

                    for item in newTrain["Schedule"]:
                        item["Time"] = self.secondsToTime(self.time_to_seconds(item["Time"])+((i+1)*self.time_to_seconds(train["RepeatInterval"])))

                    tempArray.append(newTrain)
        timetableData["Trains"] +=(tempArray)

        print(timetableData)

        self.timetableData = timetableData
        return False            
        
    def increment_with_mask(self, s, mask, increment_amount):
        result = []
        for char, m in zip(s, mask):
            if char.isdigit() and m == '+':  # If it's a digit and the mask says increment
                result.append(str(int(char) + increment_amount))
            else:
                result.append(char)  # Keep the character unchanged (either non-digit or '-')

        return ''.join(result)

    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path, 'r') as file:
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

            self.trainListTable.setItem(rowNum, 4, QTableWidgetItem(train.destination)) #FinalDestination
            self.trainListTable.setItem(rowNum, 3, QTableWidgetItem(train.sorted_schedule[-1]['Location'])) #End Section

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
            if 0 <= self.selectedTrainIndex < len(self.trainList):
                train = self.trainList[self.selectedTrainIndex]
            else:
                self.selectedTrainIndex = None
                return

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
