import json



class Timetable:
    def __init__(self,openGlInstance,shape):
        self.openGlInstance=openGlInstance
        self.shape = shape

    def openFile(self,fileName):
        #Read from the json file
        timetableData = self.load_json_from_file(fileName)

        #Extract track metadata and dimensions from loaded JSON data.
        self.map_name = timetableData["MapName"]
        self.simTime = timetableData["SimTime"]

        self.trainList = []

        trainData = timetableData["Trains"]

        for train in trainData:
            pass


    #This function opens the file.
    def load_json_from_file(self, file_path):
        with open(file_path[0], 'r') as file:
            json_data = json.load(file)
        return json_data