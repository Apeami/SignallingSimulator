
import ui_timetableEditor
from PyQt5.QtWidgets import QWidget, QFileDialog, QTimeEdit, QComboBox, QTableWidget, QDialog, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import QTime
import sys
import json
import copy


class TimetableEditor(ui_timetableEditor.Ui_Form):
    def __init__(self, mapEditor):
        print("OPEN TIMETABEL")
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)
        
        self.selectedHeadcode = None
        self.selectTrainPrev = None

        self.mapEditor = mapEditor

        self.trainListButtons = []

        self.ActionTable.setSelectionBehavior(QTableWidget.SelectRows)

    def createSkeletonTimetable(self):
        timetable = {}
        timetable["type"] = "timetable"
        timetable["name"] = "TODOTEMPNAME"
        timetable["EndTime"] = "00:00:00"
        timetable["StartTime"] = "00:00:00"

        timetable["Trains"] = []
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

        self.AddTimeButton.clicked.connect(self.addTimetableEntry)
        self.DeleteTimeButton.clicked.connect(self.removeTimetableEntry)

        self.CopyTrainButton.clicked.connect(self.copyTrain)
        self.AddOffsetButton.clicked.connect(self.addOffset)

        self.headcodeText.editingFinished.connect(self.headcodeEdited)

        self.waypoints = []
        for tile in self.mapEditor.trackData['data']:
            if 'waypoint' in tile:
                self.waypoints.append(tile['waypoint'])

        print(self.timetableData)
        self.mapNameText.setText(self.timetableData['name'])
        if 'info' in self.timetableData:
            self.infoFileText.setText(self.timetableData['info'])
        time = QTime.fromString(self.timetableData['StartTime'], "HH:mm:ss")
        self.startTimeText.setTime(time)
        time = QTime.fromString(self.timetableData['EndTime'], "HH:mm:ss")
        self.endTimeText.setTime(time)

        self.reloadTrainList()
    
    def copyTrain(self):
        for train in self.timetableData["Trains"]:
            if train["Headcode"] == self.selectedHeadcode:
                trainCopy = copy.deepcopy(train) 
                trainCopy["Headcode"] += " (Copy)"
                self.timetableData["Trains"].append(trainCopy)

        self.reloadTrainList()

    def addOffset(self):
        # Create the dialog
        dialog = QDialog()
        dialog.setWindowTitle("Time Offset Selection")

        # Create the label
        label = QLabel("Select offset")

        # Create the time edit widget
        timeEdit = QTimeEdit()
        timeEdit.setDisplayFormat("HH:mm:ss")

        # Create the checkbox for negative time offset
        negativeCheckBox = QCheckBox("Negative")

        # Create OK and Cancel buttons
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        # Connect the buttons to their respective functions
        okButton.clicked.connect(dialog.accept)
        cancelButton.clicked.connect(dialog.reject)

        # Create the layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(timeEdit)
        layout.addWidget(negativeCheckBox)

        # Create a horizontal layout for buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        # Add the button layout to the main layout
        layout.addLayout(buttonLayout)

        # Set the dialog layout
        dialog.setLayout(layout)

        # Execute the dialog and check the result
        if dialog.exec_() == QDialog.Accepted:
            print("Accepted")
            for train in self.timetableData["Trains"]:
                print(train["Headcode"])
                print(self.selectedHeadcode)
                if train["Headcode"] == self.selectedHeadcode:
                    selected_time = timeEdit.time()
                    print(selected_time.toString('HH:mm:ss'))
                    is_negative = negativeCheckBox.isChecked()
                    offset_seconds = (selected_time.hour() * 3600 +
                                    selected_time.minute() * 60 +
                                    selected_time.second())
                    if is_negative:
                        offset_seconds = -offset_seconds
                    print(offset_seconds)
                    tempCurrentTime = QTime.fromString(train["LoadTime"], "HH:mm:ss")
                    print(tempCurrentTime.toString('HH:mm:ss'))
                    tempCurrentTime = tempCurrentTime.addSecs(offset_seconds)
                    print(tempCurrentTime.toString('HH:mm:ss'))

                    train["LoadTime"] = tempCurrentTime.toString('HH:mm:ss')

                    self.reselectTrain(train["Headcode"])

                    print(self.timetableData)

    def headcodeEdited(self):
        for button in self.trainListButtons:
            print(button.text())
            print(self.selectTrainPrev["Headcode"])
            if button.text()==self.selectTrainPrev["Headcode"]:
                print("Match")
                self.selectTrainPrev["Headcode"] = self.headcodeText.text()
                button.setText(self.headcodeText.text())
        # self.reselectTrain(self.selectTrainPrev["Headcode"])
        # self.selectTrainPrev["Headcode"] = self.headcodeText.text()
        # self.reloadTrainList()
        

    def reloadTrainList(self):
        print("Reloaded")
        self.trainListButtons = []
        for i in reversed(range(self.ScrollAreaLayout.count())): 
            self.ScrollAreaLayout.itemAt(i).widget().setParent(None)
        i=0
        print("Deleted")
        for train in self.timetableData["Trains"]:
            headcode = train["Headcode"]
            button = QPushButton(headcode)
            button.clicked.connect(lambda: self.trainSelected())
            self.ScrollAreaLayout.addWidget(button)
            self.trainListButtons.append(button)
            i+=1
        print("Done")

    def addTimetableEntry(self):
        current_row_count = self.ActionTable.rowCount()
        self.ActionTable.setRowCount(current_row_count + 1)
        task = {'Action': 'None', 'Time': '00:00:00', 'Location': ''}
        self.putTaskInTable(task,current_row_count)

        for train in self.timetableData["Trains"]:
            if train["Headcode"] == self.selectedHeadcode:
                train["Schedule"].append(task)

    def removeTimetableEntry(self):
        print("remove Timetable entry")
        selected_rows = self.ActionTable.selectionModel().selectedRows()
        print(selected_rows)
        if not selected_rows:
            return

        for selected_row in sorted(selected_rows, key=lambda x: x.row(), reverse=True):
            self.ActionTable.removeRow(selected_row.row())

            for train in self.timetableData["Trains"]:
                if train["Headcode"] == self.selectedHeadcode:
                    train["Schedule"].pop(selected_row)


    def newTrain(self):
        def_data ={"Headcode": "XXX" + str(len(self.timetableData["Trains"])),
            "MaxSpeed": 0,
            "Destination": "",
            "LoadTime" : "00:00:00",
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
                

    def extractTableData(self):
        table_data = []

        for row in range(self.ActionTable.rowCount()):
            time = self.ActionTable.cellWidget(row, 0)
            time = time.time().toString()

            action = self.ActionTable.cellWidget(row, 1)
            action = action.currentText()

            waypoint = self.ActionTable.cellWidget(row, 2)
            waypoint = waypoint.currentText()

            table_data.append({ "Action": action, "Time": time, "Location": waypoint })


        return table_data

    def trainSelected(self):
        button = self.mainWidget.sender()
        headcode = button.text()
        self.reselectTrain(headcode)

    def reselectTrain(self,headcode):
        self.selectedHeadcode = headcode
        print(f"Clicked: {headcode}")

        if self.selectTrainPrev!=None:
            self.selectTrainPrev["Headcode"] = self.headcodeText.text()
            self.selectTrainPrev["Destination"] = self.destinationText.text()
            self.selectTrainPrev["LoadTime"] = self.loadTimeText.text()
            self.selectTrainPrev["MaxSpeed"] = self.maxSpeedText.text()

            print(self.extractTableData())
            data = self.extractTableData()
            self.selectTrainPrev["Schedule"] = data

        self.reloadTrainList()

        for train in self.timetableData["Trains"]:
            headcodeSel = train["Headcode"]
            if headcode == headcodeSel:
                selectTrain = train

        self.headcodeText.setText(selectTrain["Headcode"])
        self.destinationText.setText(selectTrain["Destination"])
        time = QTime.fromString(selectTrain["LoadTime"], "HH:mm:ss")
        self.loadTimeText.setTime(time)
        self.maxSpeedText.setText(str(selectTrain["MaxSpeed"]))

        self.ActionTable.setRowCount(len(selectTrain["Schedule"]))  # Set number of rows
        self.ActionTable.setColumnCount(3)  # Set number of columns
        row = 0
        for task in selectTrain["Schedule"]:
            self.putTaskInTable(task, row)
            row+=1
    
        self.selectTrainPrev = selectTrain


    def putTaskInTable(self,task, row):
        print(task)
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