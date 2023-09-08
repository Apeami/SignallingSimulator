# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.openGLWidget = PygletWidget(self.centralwidget)
        self.openGLWidget.setMinimumSize(QtCore.QSize(600, 450))
        self.openGLWidget.setObjectName("openGLWidget")
        self.gridLayout_4.addWidget(self.openGLWidget, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.TrainListBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TrainListBox.setObjectName("TrainListBox")
        self.gridLayout = QtWidgets.QGridLayout(self.TrainListBox)
        self.gridLayout.setObjectName("gridLayout")
        self.TrainList = QtWidgets.QTableWidget(self.TrainListBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrainList.sizePolicy().hasHeightForWidth())
        self.TrainList.setSizePolicy(sizePolicy)
        self.TrainList.setMinimumSize(QtCore.QSize(380, 0))
        self.TrainList.setObjectName("TrainList")
        self.TrainList.setColumnCount(6)
        self.TrainList.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.TrainList.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Headcode ")
        self.TrainList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Time")
        self.TrainList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Next Waypoint")
        self.TrainList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Destination")
        self.TrainList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainList.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainList.setItem(0, 2, item)
        self.gridLayout.addWidget(self.TrainList, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.TrainListBox)
        self.TrainInfoBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TrainInfoBox.setObjectName("TrainInfoBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.TrainInfoBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TrainTimetable = QtWidgets.QTableWidget(self.TrainInfoBox)
        self.TrainTimetable.setObjectName("TrainTimetable")
        self.TrainTimetable.setColumnCount(4)
        self.TrainTimetable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.TrainTimetable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Time")
        self.TrainTimetable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainTimetable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainTimetable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TrainTimetable.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.TrainTimetable, 1, 0, 1, 1)
        self.CurrentHeadcode = QtWidgets.QLabel(self.TrainInfoBox)
        self.CurrentHeadcode.setObjectName("CurrentHeadcode")
        self.gridLayout_2.addWidget(self.CurrentHeadcode, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.TrainInfoBox)
        self.TimingBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TimingBox.setObjectName("TimingBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.TimingBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.TimingBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lcdNumber = QtWidgets.QLCDNumber(self.TimingBox)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_3.addWidget(self.lcdNumber)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playSimulation = QtWidgets.QPushButton(self.TimingBox)
        self.playSimulation.setObjectName("playSimulation")
        self.horizontalLayout.addWidget(self.playSimulation)
        self.pauseSimulation = QtWidgets.QPushButton(self.TimingBox)
        self.pauseSimulation.setObjectName("pauseSimulation")
        self.horizontalLayout.addWidget(self.pauseSimulation)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.times1Speed = QtWidgets.QPushButton(self.TimingBox)
        self.times1Speed.setObjectName("times1Speed")
        self.horizontalLayout_2.addWidget(self.times1Speed)
        self.times2Speed = QtWidgets.QPushButton(self.TimingBox)
        self.times2Speed.setObjectName("times2Speed")
        self.horizontalLayout_2.addWidget(self.times2Speed)
        self.times5Speed = QtWidgets.QPushButton(self.TimingBox)
        self.times5Speed.setObjectName("times5Speed")
        self.horizontalLayout_2.addWidget(self.times5Speed)
        self.times10Speed = QtWidgets.QPushButton(self.TimingBox)
        self.times10Speed.setObjectName("times10Speed")
        self.horizontalLayout_2.addWidget(self.times10Speed)
        self.times20Speed = QtWidgets.QPushButton(self.TimingBox)
        self.times20Speed.setObjectName("times20Speed")
        self.horizontalLayout_2.addWidget(self.times20Speed)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.TimingBox)
        self.LogBox = QtWidgets.QGroupBox(self.centralwidget)
        self.LogBox.setObjectName("LogBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.LogBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.LogTextBox = QtWidgets.QTextEdit(self.LogBox)
        self.LogTextBox.setReadOnly(True)
        self.LogTextBox.setObjectName("LogTextBox")
        self.gridLayout_5.addWidget(self.LogTextBox, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.LogBox)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSimulation = QtWidgets.QMenu(self.menubar)
        self.menuSimulation.setObjectName("menuSimulation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRed = QtWidgets.QAction(MainWindow)
        self.actionRed.setObjectName("actionRed")
        self.actionyellow = QtWidgets.QAction(MainWindow)
        self.actionyellow.setObjectName("actionyellow")
        self.actiondYellow = QtWidgets.QAction(MainWindow)
        self.actiondYellow.setObjectName("actiondYellow")
        self.actionGreen = QtWidgets.QAction(MainWindow)
        self.actionGreen.setObjectName("actionGreen")
        self.actionToggle_Track = QtWidgets.QAction(MainWindow)
        self.actionToggle_Track.setObjectName("actionToggle_Track")
        self.actionAuto_Track = QtWidgets.QAction(MainWindow)
        self.actionAuto_Track.setObjectName("actionAuto_Track")
        self.actionRoute_Train = QtWidgets.QAction(MainWindow)
        self.actionRoute_Train.setObjectName("actionRoute_Train")
        self.actionNew_Simulation = QtWidgets.QAction(MainWindow)
        self.actionNew_Simulation.setObjectName("actionNew_Simulation")
        self.actionOpen_Map = QtWidgets.QAction(MainWindow)
        self.actionOpen_Map.setObjectName("actionOpen_Map")
        self.actionOpen_Timetable = QtWidgets.QAction(MainWindow)
        self.actionOpen_Timetable.setObjectName("actionOpen_Timetable")
        self.actionSave_Scenario = QtWidgets.QAction(MainWindow)
        self.actionSave_Scenario.setObjectName("actionSave_Scenario")
        self.actionOpen_Scenario = QtWidgets.QAction(MainWindow)
        self.actionOpen_Scenario.setObjectName("actionOpen_Scenario")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionZoom_In = QtWidgets.QAction(MainWindow)
        self.actionZoom_In.setObjectName("actionZoom_In")
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        self.actionActual_Size = QtWidgets.QAction(MainWindow)
        self.actionActual_Size.setObjectName("actionActual_Size")
        self.actionToggle_Grid = QtWidgets.QAction(MainWindow)
        self.actionToggle_Grid.setObjectName("actionToggle_Grid")
        self.actionErrors = QtWidgets.QAction(MainWindow)
        self.actionErrors.setCheckable(True)
        self.actionErrors.setObjectName("actionErrors")
        self.actionWarnings = QtWidgets.QAction(MainWindow)
        self.actionWarnings.setCheckable(True)
        self.actionWarnings.setObjectName("actionWarnings")
        self.actionDeleteRouting = QtWidgets.QAction(MainWindow)
        self.actionDeleteRouting.setObjectName("actionDeleteRouting")
        self.menuFile.addAction(self.actionNew_Simulation)
        self.menuFile.addAction(self.actionOpen_Map)
        self.menuFile.addAction(self.actionOpen_Timetable)
        self.menuFile.addAction(self.actionSave_Scenario)
        self.menuFile.addAction(self.actionOpen_Scenario)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuView.addAction(self.actionActual_Size)
        self.menuView.addAction(self.actionToggle_Grid)
        self.menuSimulation.addAction(self.actionErrors)
        self.menuSimulation.addAction(self.actionWarnings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRed)
        self.toolBar.addAction(self.actionyellow)
        self.toolBar.addAction(self.actiondYellow)
        self.toolBar.addAction(self.actionGreen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionToggle_Track)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAuto_Track)
        self.toolBar.addAction(self.actionRoute_Train)
        self.toolBar.addAction(self.actionDeleteRouting)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TrainListBox.setTitle(_translate("MainWindow", "Train List"))
        item = self.TrainList.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "End Portal"))
        item = self.TrainList.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Center"))
        __sortingEnabled = self.TrainList.isSortingEnabled()
        self.TrainList.setSortingEnabled(False)
        self.TrainList.setSortingEnabled(__sortingEnabled)
        self.TrainInfoBox.setTitle(_translate("MainWindow", "Train Information"))
        item = self.TrainTimetable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Action"))
        item = self.TrainTimetable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Location"))
        item = self.TrainTimetable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Center"))
        self.CurrentHeadcode.setText(_translate("MainWindow", "HeadCode: Not Selected"))
        self.TimingBox.setTitle(_translate("MainWindow", "Timing"))
        self.label_3.setText(_translate("MainWindow", "Simulation Time"))
        self.playSimulation.setText(_translate("MainWindow", "Play"))
        self.pauseSimulation.setText(_translate("MainWindow", "Pause"))
        self.times1Speed.setText(_translate("MainWindow", "1x"))
        self.times2Speed.setText(_translate("MainWindow", "2x"))
        self.times5Speed.setText(_translate("MainWindow", "5x"))
        self.times10Speed.setText(_translate("MainWindow", "10x"))
        self.times20Speed.setText(_translate("MainWindow", "20x"))
        self.LogBox.setTitle(_translate("MainWindow", "Event Box"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSimulation.setTitle(_translate("MainWindow", "Simulation"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionRed.setText(_translate("MainWindow", "Red"))
        self.actionyellow.setText(_translate("MainWindow", "Yellow"))
        self.actiondYellow.setText(_translate("MainWindow", "Double Yellow"))
        self.actionGreen.setText(_translate("MainWindow", "Green"))
        self.actionToggle_Track.setText(_translate("MainWindow", "Toggle Point"))
        self.actionAuto_Track.setText(_translate("MainWindow", "Auto Track"))
        self.actionRoute_Train.setText(_translate("MainWindow", "Route Train"))
        self.actionNew_Simulation.setText(_translate("MainWindow", "New Simulation"))
        self.actionOpen_Map.setText(_translate("MainWindow", "Open Map"))
        self.actionOpen_Timetable.setText(_translate("MainWindow", "Open Timetable"))
        self.actionSave_Scenario.setText(_translate("MainWindow", "Save Scenario"))
        self.actionOpen_Scenario.setText(_translate("MainWindow", "Open Scenario"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_Out.setText(_translate("MainWindow", "Zoom Out"))
        self.actionActual_Size.setText(_translate("MainWindow", "Actual Size"))
        self.actionToggle_Grid.setText(_translate("MainWindow", "Toggle Grid"))
        self.actionErrors.setText(_translate("MainWindow", "Errors"))
        self.actionWarnings.setText(_translate("MainWindow", "Warnings"))
        self.actionDeleteRouting.setText(_translate("MainWindow", "DeleteRouting"))
from pygletWidget import PygletWidget
