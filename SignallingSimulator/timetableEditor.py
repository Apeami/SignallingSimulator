
import ui_timetableEditor
from PyQt5.QtWidgets import QWidget, QFileDialog, QTimeEdit, QComboBox, QTableWidget, QDialog, QHBoxLayout,QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import QTime
import sys
import json
import copy
import os


class TimetableEditor(ui_timetableEditor.Ui_Form):
    def __init__(self, mapEditor):
        print("OPEN TIMETABEL")
        self.mainWidget = QWidget()
        self.setupUi(self.mainWidget)
        
        self.selectedHeadcode = None
        self.selectTrainPrev = None
        self.headcodeEditedDebounce = False

        self.lastTimeEntry = "00:00:00"

        self.mapEditor = mapEditor

        self.saved = True
        self.fileName = None
        self.resetTitle()

        self.trainListButtons = []

        self.ActionTable.setSelectionBehavior(QTableWidget.SelectRows)

        self.SaveButton.clicked.connect(self.save)
        self.closeButton.clicked.connect(self.closePrompt)

        self.NewTrainButton.clicked.connect(self.newTrain)
        self.DeleteTrainButton.clicked.connect(self.delTrain)

        self.AddTimeButton.clicked.connect(self.addTimetableEntry)
        self.DeleteTimeButton.clicked.connect(self.removeTimetableEntry)

        self.CopyTrainButton.clicked.connect(self.copyTrain)
        self.AddOffsetButton.clicked.connect(self.addOffset)

        # self.loadTimeText.editingFinished.connect(lambda: self.reselectTrain(self.selectTrainPrev["Headcode"]))

        self.headcodeText.editingFinished.connect(self.headcodeEdited)

    def closePrompt(self):
        if self.saved == False:
            reply = QMessageBox.question(self.mainWidget, 'Message',
                "There are unsaved changes. Do you want to save them?", 
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save()
                self.mainWidget.close()
            elif reply == QMessageBox.Discard:
                self.mainWidget.close()
        else:
            self.mainWidget.close()

    def resetTitle(self):

        if self.fileName == None:
            file = "Untitled"
        else:
            file = os.path.basename(self.fileName)
        if self.saved == False:
            newTitle = file + "* - Timetable Editor" 
        else:
            newTitle = file + " - Timetable Editor" 
        self.mainWidget.setWindowTitle(newTitle)

    def createSkeletonTimetable(self):
        timetable = {}
        timetable["type"] = "timetable"
        timetable["name"] = "TODOTEMPNAME"
        timetable["EndTime"] = "00:00:00"
        timetable["StartTime"] = "00:00:00"

        timetable["Trains"] = []
        return timetable

    def open(self, isNew):
        print("Opening File")
        print(isNew)
        print(self)
        self.saved = True
        self.resetTitle()
        

        self.ActionTable.clearContents()
        column_names = ["Time", "Action", "Waypoint"]
        self.ActionTable.setHorizontalHeaderLabels(column_names)

        self.ActionTable.setRowCount(0)
        self.ActionTable.setColumnCount(0)

        if not isNew:
            self.fileName = QFileDialog.getOpenFileName(self.mainWidget, "Open File", "", "All Files (*);;Text Files (*.txt)")[0]
            if self.fileName=='':
                return
            self.timetableData = self.load_json_from_file(self.fileName)

            if self.mapEditor.trackData['name']!= self.timetableData['name']:
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setWindowTitle("Error")
                error_dialog.setText("The Names of the map and timetable do not match. Do you want to update")
                error_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                result = error_dialog.exec_()
                if result == QMessageBox.Ok:
                    self.timetableData['name'] = self.mapEditor.trackData['name']
                else:
                    return


        else:
            self.fileName = None
            self.timetableData = self.createSkeletonTimetable()


        self.waypoints = []
        for tile in self.mapEditor.trackData['data']:
            if 'waypoint' in tile:
                if tile['waypoint'] not in self.waypoints:
                    self.waypoints.append(tile['waypoint'])

        for train in self.timetableData["Trains"]:
            for action in train["Schedule"]:
                if action["Location"] not in self.waypoints:
                    self.waypoints.append(action["Location"])

        self.mapNameText.setText(self.timetableData['name'])

        if 'info' in self.timetableData:
            self.infoFileText.setText(self.timetableData['info'])
        time = QTime.fromString(self.timetableData['StartTime'], "HH:mm:ss")
        self.startTimeText.setTime(time)
        time = QTime.fromString(self.timetableData['EndTime'], "HH:mm:ss")
        self.endTimeText.setTime(time)

        self.reloadTrainList()
        self.mainWidget.show()
    
    def copyTrain(self):
        for train in self.timetableData["Trains"]:
            if train["Headcode"] == self.selectedHeadcode:
                trainCopy = copy.deepcopy(train) 
                trainCopy["Headcode"] += " (Copy)"
                self.timetableData["Trains"].append(trainCopy)

        self.reloadTrainList()

    def addOffset(self):
        self.saved = False
        self.resetTitle()
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
            selected_time = timeEdit.time()
            is_negative = negativeCheckBox.isChecked()
            offset_seconds = (selected_time.hour() * 3600 +
                                    selected_time.minute() * 60 +
                                    selected_time.second())
            if is_negative:
                offset_seconds = -offset_seconds

            #Offset seconds is applied to all elements
            tempCurrentTime = QTime.fromString(self.loadTimeText.text(), "HH:mm:ss")
            tempCurrentTime = tempCurrentTime.addSecs(offset_seconds)
            self.loadTimeText.setTime(tempCurrentTime)

            for i in range(self.ActionTable.rowCount()):
                tempCurrentTime = QTime.fromString(self.ActionTable.cellWidget(i, 0).text(), "HH:mm:ss")
                tempCurrentTime = tempCurrentTime.addSecs(offset_seconds)
                time_edit = QTimeEdit(self.mainWidget)
                time_edit.setTime(tempCurrentTime)
                time_edit.setDisplayFormat("HH:mm:ss")
                self.ActionTable.setCellWidget(i, 0, time_edit)


                    # self.reselectTrain(train["Headcode"])



    def headcodeEdited(self):
        if self.headcodeEditedDebounce == False:
            print("Headcode Edited")
            for button in self.trainListButtons: #IF there is a duplicate headcode
                if button.text() == self.headcodeText.text():
                    self.headcodeEditedDebounce = True
                    print("Setting Test")
                    print(self.selectTrainPrev["Headcode"])
                    self.headcodeText.setText(self.selectTrainPrev["Headcode"]) 
                    error_dialog = QMessageBox()
                    error_dialog.setIcon(QMessageBox.Critical)
                    error_dialog.setWindowTitle("Error")
                    error_dialog.setText("You have chosen a duplicate headcode")
                    error_dialog.setStandardButtons(QMessageBox.Ok)
                    error_dialog.exec_()

                    return
            for button in self.trainListButtons:
                if button.text()==self.selectTrainPrev["Headcode"]:
                    self.selectTrainPrev["Headcode"] = self.headcodeText.text()
                    button.setText(self.headcodeText.text())
        else:
            self.headcodeEditedDebounce = False
        # self.reselectTrain(self.selectTrainPrev["Headcode"])
        # self.selectTrainPrev["Headcode"] = self.headcodeText.text()
        # self.reloadTrainList()
        

    def reloadTrainList(self):
        self.saved = False
        self.resetTitle()
        self.trainListButtons = []
        for i in reversed(range(self.ScrollAreaLayout.count())): 
            self.ScrollAreaLayout.itemAt(i).widget().setParent(None)

        i=0
        sortedTrainList = sorted(self.timetableData["Trains"], key=lambda train: train["LoadTime"])
        for train in sortedTrainList:
            headcode = train["Headcode"]
            button = QPushButton(headcode)
            button.clicked.connect(lambda: self.trainSelected())
            self.ScrollAreaLayout.addWidget(button)
            self.trainListButtons.append(button)
            i+=1

    def addTimetableEntry(self):
        self.saved = False
        self.resetTitle()
        current_row_count = self.ActionTable.rowCount()
        self.saveCurrentlyEditedTrainData()
        # self.ActionTable.setRowCount(current_row_count + 1)

        task = {'Action': 'None', 'Time': '00:00:00', 'Location': ''}

        selected_rows = self.ActionTable.selectionModel().selectedRows()
        if not selected_rows:
            indexAfter = -1
        else:
            indexAfter = selected_rows[0].row()+1

        try:
            timeNew = self.selectTrainPrev["Schedule"][indexAfter-1]["Time"]
        except:
            timeNew = "00:00:00"
        task = {'Action': 'None', 'Time': timeNew, 'Location': ''}

        # self.putTaskInTable(task,indexAfter)
        self.saveCurrentlyEditedTrainData()
        for train in self.timetableData["Trains"]:
            if train["Headcode"] == self.selectedHeadcode:

                print("INDEX AFTER")
                print(indexAfter)
                
                train["Schedule"].insert(indexAfter, task)

                print(train["Schedule"])
                column_names = ["Time", "Action", "Waypoint"]
                self.ActionTable.setHorizontalHeaderLabels(column_names)
                self.ActionTable.setRowCount(len(train["Schedule"]))
                row=0
                for task in train["Schedule"]:
                    self.putTaskInTable(task, row)
                    row+=1

        
                    

    def removeTimetableEntry(self):
        self.saved = False
        self.resetTitle()
        selected_rows = self.ActionTable.selectionModel().selectedRows()
        if not selected_rows:
            return

        for selected_row in sorted(selected_rows, key=lambda x: x.row(), reverse=True):
            self.ActionTable.removeRow(selected_row.row())

            for train in self.timetableData["Trains"]:
                if train["Headcode"] == self.selectedHeadcode:
                    train["Schedule"].pop(selected_row.row())


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

    def saveCurrentlyEditedTrainData(self):
        if self.selectTrainPrev!=None:
            self.selectTrainPrev["Headcode"] = self.headcodeText.text()
            self.selectTrainPrev["Destination"] = self.destinationText.text()
            self.selectTrainPrev["LoadTime"] = self.loadTimeText.text()
            self.selectTrainPrev["MaxSpeed"] = self.maxSpeedText.text()

            data = self.extractTableData()
            self.selectTrainPrev["Schedule"] = data

    def reselectTrain(self,headcode):
        self.selectedHeadcode = headcode

        self.saveCurrentlyEditedTrainData()

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
        column_names = ["Time", "Action", "Waypoint"]
        self.ActionTable.setHorizontalHeaderLabels(column_names)
        row = 0
        for task in selectTrain["Schedule"]:
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
        self.saveCurrentlyEditedTrainData()
        self.saved = True
        self.resetTitle()
        if self.fileName == None:
            self.fileName = QFileDialog.getSaveFileName(self.mainWidget, "Create New File", "", "All Files (*);;Text Files (*.txt)")[0]

        self.timetableData['name'] = self.mapNameText.text()
        self.timetableData['info'] = self.infoFileText.text()
        self.timetableData['StartTime'] = self.startTimeText.text()
        self.timetableData['EndTime'] = self.endTimeText.text()

        with open(self.fileName, 'w') as file:
            json.dump(self.timetableData, file, indent=4)
        
        

    def load_json_from_file(self, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data