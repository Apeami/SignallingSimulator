
import ui_timetableEditor
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidgetItem
import sys
import json


class TimetableEditor(ui_timetableEditor.Ui_Form):
    def __init__(self, mapEditor):
        print("OPEN TIMETABEL")
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)
        
        self.selectedHeadcode = None
        
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
            self.fileName = QFileDialog.getOpenFileName(self.mainWidget, "Open File", "", "All Files (*);;Text Files (*.txt)")
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
        pass

    def removeTimetableEntry(self):
        pass

    def editTrain(self):
        pass

    def newTrain(self):
        pass

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

        for train in self.timetableData["Trains"]:
            headcodeSel = train["Headcode"]
            if headcode == headcodeSel:
                selectTrain = train

        self.ActionTable.setRowCount(len(selectTrain["Schedule"]))  # Set number of rows
        self.ActionTable.setColumnCount(3)  # Set number of columns
        row = 0
        print(selectTrain)
        for task in selectTrain["Schedule"]:
            print(task)
            self.ActionTable.setItem(row, 0, QTableWidgetItem(task["Time"]))
            self.ActionTable.setItem(row, 1, QTableWidgetItem(task["Action"]))
            self.ActionTable.setItem(row, 2, QTableWidgetItem(task["Location"]))

            row+=1

    def save(self):
        if self.fileName == None:
            self.fileName = QFileDialog.getSaveFileName(self.mainWidget, "Create New File", "", "All Files (*);;Text Files (*.txt)")[0]

        with open(self.fileName, 'w') as file:
            json.dump(self.timetableData, file, indent=4)
        
        self.mainWidget.close()

    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data