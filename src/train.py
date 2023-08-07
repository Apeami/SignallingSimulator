

class train:
    def __init__(self,trainData):
        self.headcode = trainData['Headcode']
        self.maxSpeed = trainData['MaxSpeed']

        self.sorted_schedule = sorted(trainData["Schedule"], key=lambda x: x["Time"])

        self.currentEvent = 0

    def updateMajorEvent(self):
        pass

    def updateMinorEvent(self):
        pass