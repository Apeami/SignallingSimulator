import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QDialog, QScrollArea, QVBoxLayout, QTextEdit

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set up the window
        self.setWindowTitle('Welcome to Signalling Simulator')
        self.setGeometry(100, 100, 300, 200)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Welcome label
        welcome_label = QLabel('Welcome to Signalling Simulator', self)
        layout.addWidget(welcome_label)
        
        # Open Timetable button
        open_timetable_btn = QPushButton('Open Timetable', self)
        open_timetable_btn.clicked.connect(self.openTimetable)
        layout.addWidget(open_timetable_btn)
        
        # Open Map button
        open_map_btn = QPushButton('Open Map', self)
        open_map_btn.clicked.connect(self.openMap)
        layout.addWidget(open_map_btn)
        
        # Help button
        help_btn = QPushButton('Help', self)
        help_btn.clicked.connect(lambda: self.showHelp(self))
        layout.addWidget(help_btn)
        
        # Set layout
        self.setLayout(layout)
    
    def openTimetable(self):
        # Open file dialog to select a timetable file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Timetable", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f"Selected timetable: {file_name}")
    
    def openMap(self):
        # Open file dialog to select a map file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Map", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f"Selected map: {file_name}")
    
    def showHelp(self, mainwindow):
        # Display help information in a custom scrollable dialog
        help_text = """
        <h1>Railway Signalling Simulator Help Guide</h1>
        <p>Welcome to the Railway Signalling Simulator! This guide will introduce you to the features of the Graphical User Interface (GUI) and help you get started with managing and routing trains effectively.</p>
        
        <h2>Overview of the GUI</h2>
        <p>The GUI of the Railway Signalling Simulator is divided into several sections, each serving a specific purpose in train management and signalling. Below is a description of each section and its functionalities.</p>
        
        <h3>Menu Bar</h3>
        <ul>
        <li><b>File:</b> Contains options related to file operations, such as opening and saving simulations.</li>
        <li><b>View:</b> Offers options to customize the view of the simulation.</li>
        <li><b>Simulation:</b> Provides controls to start, stop, and manage the simulation.</li>
        </ul>
        
        <h3>Toolbar</h3>
        <ul>
        <li><b>Red:</b> Set signals to red.</li>
        <li><b>Yellow:</b> Set signals to yellow.</li>
        <li><b>Double Yellow:</b> Set signals to double yellow.</li>
        <li><b>Green:</b> Set signals to green.</li>
        <li><b>Toggle Point:</b> Change the position of railway points/switches.</li>
        <li><b>Auto Track:</b> Automatically tracks trains in the simulation.</li>
        <li><b>Route Train:</b> Route a train to a specified destination.</li>
        <li><b>DeleteRouting:</b> Remove an existing routing.</li>
        </ul>
        
        <h3>Main Display Area</h3>
        <p>This is the primary area where the track layout is displayed. It shows the positions of trains, signals, and switches. The track layout consists of the following elements:</p>
        <ul>
        <li><b>White Lines:</b> Represent the tracks.</li>
        <li><b>Red Circles:</b> Indicate red signals.</li>
        <li><b>Yellow Circles:</b> Indicate yellow signals.</li>
        <li><b>Green Circles:</b> Indicate green signals.</li>
        <li><b>Dashed Lines:</b> Represent track segments that can be toggled for routing trains.</li>
        <li><b>Blue Rectangles:</b> Represent portals for train entry and exit.</li>
        <li><b>Pink Rectangles:</b> Represent important stations or junctions.</li>
        <li><b>Train Labels:</b> Each train is labeled with its headcode (e.g., "2H26") for easy identification.</li>
        </ul>
        
        <h3>Train List</h3>
        <p>The Train List section displays the list of trains currently in the simulation with the following details:</p>
        <ul>
        <li><b>Next Waypoint:</b> The next waypoint or station the train is heading to.</li>
        <li><b>Destination:</b> The final destination of the train.</li>
        <li><b>End Portal:</b> The portal through which the train will exit the simulation.</li>
        </ul>
        
        <h3>Train Information</h3>
        <p>The Train Information section provides detailed information about a selected train, including:</p>
        <ul>
        <li><b>Headcode:</b> The train's identification code.</li>
        <li><b>Time:</b> The scheduled time for each action.</li>
        <li><b>Action:</b> The action to be taken (e.g., Spawn, Despawn).</li>
        <li><b>Location:</b> The location where the action takes place.</li>
        <li><b>Center:</b> Additional details about the train's position or status.</li>
        </ul>
        
        <h3>Timing Controls</h3>
        <p>The Timing Controls section allows you to control the simulation's time flow:</p>
        <ul>
        <li><b>Play:</b> Start or resume the simulation.</li>
        <li><b>Pause:</b> Pause the simulation.</li>
        <li><b>1x, 2x, 5x, 10x, 20x:</b> Adjust the simulation speed.</li>
        </ul>
        
        <h3>Event Box</h3>
        <p>The Event Box displays a log of recent events and actions taken in the simulation, such as starting the simulator, opening maps, and loading timetables.</p>
        
        <h2>Getting Started</h2>
        <p>Follow these steps to get started:</p>
        <ol>
        <li><b>Start the Simulator:</b> Use the options in the Simulation menu to start the simulator.</li>
        <li><b>Open a Map:</b> Load a track layout from the File menu.</li>
        <li><b>Load a Timetable:</b> Open a timetable to schedule trains.</li>
        <li><b>Manage Signals:</b> Use the toolbar to change signal states and control train movements.</li>
        <li><b>Route Trains:</b> Select a train and use the Route Train button to set its path.</li>
        <li><b>Monitor Trains:</b> Keep an eye on the Train List and Train Information sections to manage train operations effectively.</li>
        <li><b>Control Simulation Time:</b> Adjust the simulation speed using the Timing Controls to speed up or slow down the simulation as needed.</li>
        </ol>
        
        <h2>Tips</h2>
        <ul>
        <li>Regularly check the Event Box for important notifications.</li>
        <li>Use the Toggle Point feature to change track directions and manage train routes.</li>
        <li>Adjust signals appropriately to prevent collisions and ensure smooth train operations.</li>
        </ul>
        
        <p>We hope this guide helps you navigate and utilize the Railway Signalling Simulator effectively. Enjoy managing your railway network!</p>
        """
        
        help_dialog = QDialog(mainwindow)
        help_dialog.setWindowTitle("Help")
        help_dialog.setGeometry(100, 100, 600, 400)
        
        scroll_area = QScrollArea(help_dialog)
        scroll_area.setWidgetResizable(True)
        
        help_content = QTextEdit()
        help_content.setHtml(help_text)
        help_content.setReadOnly(True)
        
        scroll_area.setWidget(help_content)
        
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
