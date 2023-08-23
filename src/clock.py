from PyQt5.QtCore import QTimer, QTime



class Clock:
    def __init__(self, ui):
        self.ui = ui

        #initialize buttons
        self.lcd = ui.lcdNumber

        self.playButton = self.ui.playSimulation
        self.playButton.clicked.connect(self.start_timer)
        self.pauseButton = self.ui.pauseSimulation
        self.pauseButton.clicked.connect(self.stop_timer)

        self.times1Button = self.ui.times1Speed
        self.times1Button.clicked.connect(lambda: self.change_speed(1))
        self.times2Button = self.ui.times2Speed
        self.times2Button.clicked.connect(lambda: self.change_speed(2))
        self.times5Button = self.ui.times5Speed
        self.times5Button.clicked.connect(lambda: self.change_speed(5))
        self.times10Button = self.ui.times10Speed
        self.times10Button.clicked.connect(lambda: self.change_speed(10))
        self.times20Button = ui.times20Speed
        self.times20Button.clicked.connect(lambda: self.change_speed(20))

        print("Setup")

        # Initialize variables
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lcd)
        self.speed = 1
        self.counter = 0

        #Manage initial time
        initial_time = QTime(7, 30, 00)
        self.counter = initial_time.hour() * 3600 + initial_time.minute() * 60 + initial_time.second()


    def start_timer(self):
        self.timer.start(1000 // self.speed)  # Adjust the interval based on speed


    def stop_timer(self):
        self.timer.stop()

    def change_speed(self, speed):
        print(speed)
        self.speed = speed
        if self.timer.isActive():
            self.timer.start(1000 // self.speed)

    def update_lcd(self):
        self.counter += 1
        time = QTime(0, 0).addSecs(self.counter)
        time_str = time.toString("hh:mm:ss")
        self.lcd.display(time_str)
        print("Second Tick")