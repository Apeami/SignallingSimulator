
import ui_timetableEditor
from PyQt5.QtWidgets import QWidget, QFileDialog, QTimeEdit, QComboBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidgetItem
from PyQt5.QtCore import QTime
import sys
import json


class TimetableEditor(ui_timetableEditor.Ui_Form):
    def __init__(self, mapEditor):
        print("OPEN TIMETABEL")
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)
        
        self.selectedHeadcode = None
        self.selectTrainPrev = None

        self.mapEditor = mapEditor

    def createSkeletonTimetable(self):
        timetable = {}
        timetable["type"] = "timetable"
        timetable["name"] = "TODOTEMPNAME"

        timetable["Trains"] = [{
            "Headcode": "2H26",
            "MaxSpeed": 75,
            "Destination": "Cambridge",
            "LoadTime" : "12:01:00",
            "Schedule": [
                { "Action": "Spawn", "Time": "12:02:00", "Location": "Liverpool Street Portal Fast In" },
                { "Action": "Despawn", "Time": "12:05:00", "Location": "Clapton Portal Out" }
            ]
        },
        {
            "Headcode": "2H25",
            "MaxSpeed": 75,
            "Destination": "London Liverpool Street",
            "LoadTime" : "12:05:00",
            "Schedule": [
                { "Action": "Spawn", "Time": "12:06:00", "Location": "Clapton Portal In" },
                { "Action": "Despawn", "Time": "12:09:00", "Location": "Liverpool Street Portal Fast Out" }
            ]
        },]
        return timetable

    def open(self, isNew):
        self.mainWidget.show()

        self.ActionTable.clearContents()

        self.ActionTable.setRowCount(0)
        self.ActionTable.setColumnCount(0)

        if not isNew:
            self.fileName = QFileDialog.getOpenFileName(self.mainWidget, "Open File", "", "All Files (*);;Text Files (*.txt)")[0]
            if self.fileName==('', ''):
                return
            self.timetableData = self.load_json_from_file(self.fileName)
        else:
            self.fileName = None
            self.timetableData = self.createSkeletonTimetable()

        self.SaveCloseButton.clicked.connect(self.save)

        self.NewTrainButton.clicked.connect(self.newTrain)
        self.DeleteTrainButton.clicked.connect(self.delTrain)
        self.EditTrainButton.clicked.connect(self.editTrain)

        self.AddTimeButton.clicked.connect(self.addTimetableEntry)
        self.DeleteTimeButton.clicked.connect(self.removeTimetableEntry)

        self.waypoints = []
        for tile in self.mapEditor.trackData['data']:
            if 'waypoint' in tile:
                self.waypoints.append(tile['waypoint'])

        self.mapNameText.setText(self.timetableData['name'])
        self.infoFileText.setText(self.timetableData['info'])
        self.startTimeText.setText(self.timetableData['StartTime'])
        self.endTimeText.setText(self.timetableData['EndTime'])

        self.reloadTrainList()
    
    def reloadTrainList(self):
        for i in reversed(range(self.ScrollAreaLayout.count())): 
            self.ScrollAreaLayout.itemAt(i).widget().setParent(None)
        i=0
        for train in self.timetableData["Trains"]:
            headcode = train["Headcode"]
            button = QPushButton(headcode)
            button.clicked.connect(lambda: self.trainSelected())
            self.ScrollAreaLayout.addWidget(button)
            i+=1

    def addTimetableEntry(self):
        current_row_count = self.ActionTable.rowCount()
        self.ActionTable.setRowCount(current_row_count + 1)
        task = {'Action': 'None', 'Time': '00:00:00', 'Location': ''}
        self.putTaskInTable(task,current_row_count)

    def removeTimetableEntry(self):
        pass

    def editTrain(self):
        pass

    def newTrain(self):
        def_data ={"Headcode": "XXX" + str(len(self.timetableData["Trains"])),
            "MaxSpeed": 0,
            "Destination": "",
            "LoadTime" : "xx:xx:xx",
            "Schedule": []
        }
        self.timetableData["Trains"].append(def_data)
        self.reloadTrainList()

    def delTrain(self):
        if self.selectedHeadcode !=None:
            for train in self.timetableData["Trains"]:
                headcodeSel = train["Headcode"]
                if self.selectedHeadcode == headcodeSel:
                    self.timetableData["Trains"].remove(train)
                    self.reloadTrainList()
                

    def trainSelected(self):
        button = self.mainWidget.sender()
        headcode = button.text()
        self.selectedHeadcode = headcode
        print(f"Clicked: {headcode}")

        if self.selectTrainPrev!=None:
            self.selectTrainPrev["Headcode"] = self.headcodeText.text()
            self.selectTrainPrev["Destination"] = self.destinationText.text()
            self.selectTrainPrev["LoadTime"] = self.loatTimeText.text()
            self.selectTrainPrev["MaxSpeed"] = self.maxSpeedText.text()

        for train in self.timetableData["Trains"]:
            headcodeSel = train["Headcode"]
            if headcode == headcodeSel:
                selectTrain = train

        self.headcodeText.setText(selectTrain["Headcode"])
        self.destinationText.setText(selectTrain["Destination"])
        self.loatTimeText.setText(selectTrain["LoadTime"])
        self.maxSpeedText.setText(str(selectTrain["MaxSpeed"]))

        self.ActionTable.setRowCount(len(selectTrain["Schedule"]))  # Set number of rows
        self.ActionTable.setColumnCount(3)  # Set number of columns
        row = 0
        print(selectTrain)
        for task in selectTrain["Schedule"]:
            print(task)
            self.putTaskInTable(task, row)
            row+=1
    
        self.selectTrainPrev = selectTrain


    def putTaskInTable(self,task, row):
        time = QTime.fromString(task['Time'], "HH:mm:ss")
        time_edit = QTimeEdit(self.mainWidget)
        time_edit.setTime(time)
        time_edit.setDisplayFormat("HH:mm:ss")
        self.ActionTable.setCellWidget(row, 0, time_edit)

        actions = ["Spawn", "Call", "Despawn", "None"]
        combo_box = QComboBox(self.mainWidget)
        combo_box.addItems(actions)
        index = combo_box.findText(task["Action"])
        if index != -1:
            combo_box.setCurrentIndex(index)
        self.ActionTable.setCellWidget(row, 1, combo_box)

        combo_box = QComboBox(self.mainWidget)
        combo_box.addItems(self.waypoints)
        index = combo_box.findText(task["Location"])
        if index != -1:
            combo_box.setCurrentIndex(index)
        self.ActionTable.setCellWidget(row, 2, combo_box)

    def save(self):
        if self.fileName == None:
            self.fileName = QFileDialog.getSaveFileName(self.mainWidget, "Create New File", "", "All Files (*);;Text Files (*.txt)")[0]

        self.timetableData['name'] = self.mapNameText.text()
        self.timetableData['info'] = self.infoFileText.text()
        self.timetableData['StartTime'] = self.startTimeText.text()
        self.timetableData['EndTime'] = self.endTimeText.text()

        with open(self.fileName, 'w') as file:
            json.dump(self.timetableData, file, indent=4)
        
        self.mainWidget.close()

    def load_json_from_file(self, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data