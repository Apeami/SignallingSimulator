from extra import WarningBox
from tileBase import *


class AbstractTrackSection:
    def __init__(self,firstTile,secondTile,tileMapper):
        self.firstTile = firstTile
        self.secondTile = secondTile
        self.tileMapper = tileMapper
        self.active = True
        self.success = True
        self.tileList = []

        print(firstTile)
        print(firstTile.tileCoord)
        print(secondTile)
        print(secondTile.tileCoord)
        if not isinstance(firstTile, SignalTile) or not isinstance(secondTile,SignalTile):
            self.active = False
            self.success =False
            print("Cann ot auto Track")
            WarningBox("The first and last tiles are not signals","Cannot complete").exec_()
            
            
            
        
    def deleteIfSelected(self,selectedTile):
        for tile in self.tileList:
            if tile==selectedTile:
                self.delete()
                return True
        return False

    def delete(self):
        print("Deleting")
        self.active = False
        for tile in self.tileList:
            tile.changeColor((255,255,255))
            if isinstance(tile, SignalTile):
                tile.lock =False
                tile.firstRouteSignal = False
                tile.lastRouteSignal = False

        self.tileMapper.updateSignals()

class AutoTrack(AbstractTrackSection):
    def __init__(self,firstTile,secondTile,tileMapper):
        self.success = True
        super().__init__(firstTile,secondTile,tileMapper)

        if self.active ==True:
            self.tileList.append(firstTile)  
            startDir = self.firstTile.getDefaultStartDir()
            newTile = self.tileMapper.tileMap[self.firstTile.tileCoord[1]+startDir[0]][self.firstTile.tileCoord[0]+startDir[1]]
            entryDir = (-startDir[0], -startDir[1])

            timerOut = 0
            while newTile!=secondTile and timerOut<100:

                if isinstance(newTile,PointTile):
                    self.delete()
                    WarningBox("Cannot Find a route for auto track","Cannot Complete").exec_()
                    self.success = False
                
                if isinstance(newTile,PointTile):
                    defaultDir = newTile.getDefaultStartDir()
                    #Temp Bug

                self.tileList.append(newTile)


                coords = newTile.getEntryAndExitCoord(entryDir,False)
                for testCoord in coords:
                    if testCoord!=entryDir:
                        coord = testCoord
                newTileCoordX = newTile.tileCoord[0] + coord[1]
                newTileCoordY = newTile.tileCoord[1] + coord[0]

                newTile = self.tileMapper.tileMap[newTileCoordY][newTileCoordX]
                entryDir = (-coord[0],-coord[1])
                timerOut = timerOut +1 

            self.tileList.append(secondTile)


    def createRouting(self):
        if self.active:
            for tile in self.tileList:
                tile.changeColor((0,255,255))
                if isinstance(tile,SignalTile):
                    if tile== self.secondTile:
                        tile.lastRouteSignal = True
                        tile.lock=False
                    else:
                        tile.firstRouteSignal = True
                        tile.lock = True

            self.tileMapper.updateSignals()


class BranchSignalTile:
    def __init__(self,tileMapper):
        self.tileMapper = tileMapper

    def findNextSignal(self, tile, tileDirection, visited=None):

        if visited is None:
            visited = set()

        if tile is None or tile.tileCoord in visited:
            return []

        print("FINDING NEXT SIGNAL")
        print("TileLocation")
        print(tile.tileCoord)
        print("Search Direction")
        print(tileDirection)

        visited.add(tile.tileCoord)

        if isinstance(tile, SignalTile):
            if (tile.getDefaultStartDir() == tileDirection):
                print("ReturningTile")
                print(tile.tileCoord)
                return [tile]
        if isinstance(tile,PortalTile):
            return []

        entryDir = (-tileDirection[0], -tileDirection[1])

        coords = tile.getEntryAndExitCoord(entryDir=entryDir,currentStatus=False)

        print("directional Coords")
        print(coords)
        print("entry Dir")
        print(entryDir)

        tileList = []
        for coord in coords:
            if coord != entryDir:
                newTileCoordX = tile.tileCoord[0] + coord[1]
                newTileCoordY = tile.tileCoord[1] + coord[0]

                try:#Catching index out of range
                    newTile = self.tileMapper.tileMap[newTileCoordY][newTileCoordX]
                except:
                    return []
                print("Calling Function")
                print("Direction Coord")
                print(coord)
                print("X")
                print(newTileCoordX)
                print("Y")
                print(newTileCoordY)
                result = self.findNextSignal(newTile, coord, visited=visited)
                #result = []
                for i in result:
                    tileList.append(i)

        return tileList


    def getSignalList(self,tile):
        print("GETTING SIGNAL LIST")
        print(tile.tileCoord)
        startDir = tile.getDefaultStartDir()
        entryLoc = (startDir[0],startDir[1])
        newTile = self.tileMapper.tileMap[tile.tileCoord[1]+startDir[0]][tile.tileCoord[0]+startDir[1]]
        return self.findNextSignal(newTile,entryLoc)

class RoutingTrack(AbstractTrackSection):
    def __init__(self,firstTile,secondTile,tileMapper):
        self.success = True
        AbstractTrackSection.__init__(self,firstTile,secondTile,tileMapper)

        if self.active ==False:
            self.success = False
            return

        self.tileList = self.findSignalPath(firstTile,secondTile)

        if self.tileList!=None:
            pathListTemp = self.tileList
            self.tileList = []
            for item in pathListTemp:
                if item not in self.tileList:
                    self.tileList.append(item)

            for tile in self.tileList:
                if isinstance(tile,SignalTile):
                    if tile!= self.secondTile:
                        if tile.trainInBlock==True:
                            self.success = False
                            WarningBox("There is a train in the area","Cannot complete").exec_()


            print(self.tileList)
        else:
            self.success = False
            WarningBox("Cannot find route or there is too many signals in the route","Cannot complete").exec_()


    def createRouting(self):
        if self.active:
            for i in range(len(self.tileList)):
                tile = self.tileList[i]
                tile.changeColor((0,0,255))
                print(tile.tileCoord)

                if isinstance(tile,SignalTile):
                    if tile== self.secondTile:
                        tile.lastRouteSignal = True
                        tile.lock=False
                    else:
                        tile.firstRouteSignal = True
                        tile.lock = True

                if isinstance(tile, PointTile):
                    nextTile = self.tileList[i+1]
                    prevTile = self.tileList[i-1]

                    nextTileOffset = (nextTile.tileCoord[0]-tile.tileCoord[0],nextTile.tileCoord[1]-tile.tileCoord[1])
                    prevTileOffset = (prevTile.tileCoord[0]-tile.tileCoord[0],prevTile.tileCoord[1]-tile.tileCoord[1])

                    straightCoord = tile.getEntryAndExitCoord(currentStatus=True,diverge=False)
                    curveCoord = tile.getEntryAndExitCoord(currentStatus=True,diverge=True)

                    nextTileOffset = (nextTileOffset[1],nextTileOffset[0])
                    prevTileOffset = (prevTileOffset[1],prevTileOffset[0])

                    print("POINT IS CHANGING")
                    print(tile.tileCoord)
                    print(nextTileOffset)
                    print(prevTileOffset)
                    print(straightCoord)
                    print(curveCoord)

                    if nextTileOffset in straightCoord and prevTileOffset in straightCoord:
                        print("Straight point")
                        tile.updatePoint(False)
                    if nextTileOffset in curveCoord and prevTileOffset in curveCoord:
                        tile.updatePoint(True)
                        print("CurvePoint")


            self.redSignals = []

            signalList = self.getSignalList(self.firstTile, blocking=True)
            print(signalList)
            for signal in signalList:
                if signal!=self.secondTile:
                    self.redSignals.append(signal)
                    signal.changeColor((0,255,0))



            for redSignal in self.redSignals:
                redSignal.setSignal("Red", "Router")
                redSignal.lock = True

            self.secondTile.setTrainPassedAlert(self.delete)

            self.tileMapper.updateSignals()


#Find Route between the signals
    def findSignalPath(self,firstSignal,secondSignal):
        startDir = firstSignal.getDefaultStartDir()
        entryLoc = (startDir[0],startDir[1])
        newTile = self.tileMapper.tileMap[firstSignal.tileCoord[1]+startDir[0]][firstSignal.tileCoord[0]+startDir[1]]
        print("FINGING NEXT SIGNAL PATH")
        path = self.findNextSignalPath(newTile,entryLoc, secondSignal)
        if path!=None:
            path.append(newTile)
            return path+[firstSignal]
        else:
            return None
    
    def findNextSignalPath(self, tile, tileDirection,targetTile, visited=None):

        if visited is None:
            visited = set()

        if tile is None or tile.tileCoord in visited:
            return None

        visited.add(tile.tileCoord)

        if isinstance(tile, SignalTile):
            if tile == targetTile:
                print("TILE IS RETURNED")
                print(tile.tileCoord)
                return [tile]

        entryDir = (-tileDirection[0], -tileDirection[1])
        coords = tile.getEntryAndExitCoord(entryDir,False)


        resultList = []
        for coord in coords:
            if coord != entryDir:
                newTileCoordX = tile.tileCoord[0] + coord[1]
                newTileCoordY = tile.tileCoord[1] + coord[0]

                try:#Catching index out of range
                    newTile = self.tileMapper.tileMap[newTileCoordY][newTileCoordX]
                except:
                    return None


                result = self.findNextSignalPath(newTile, coord,targetTile, visited)
                print("ITERATION RESULT")
                print(tile.tileCoord)
                print("RESULT")
                print(result)
                if result!=None:
                    print("RESULT APPENDED")
                    print(result)
                    print(tile)
                    print(result.append(tile))
                     
                    if isinstance(tile,SignalTile):
                        defaultDir = tile.getDefaultStartDir()
                        print("SIGNAL TILE IN WAY")
                        print(defaultDir)
                        print(tileDirection)

                        if defaultDir == entryDir: #If signal is in opposite direction
                            result.append(tile)
                            return result
                        else:
                            return None #Signal is in same direction 
                    else:
                        result.append(tile) #There is no Signal
                        return result 

        return None


#Find the signals to turn red
    def findNextSignal(self, tile, tileDirection, visited=None, blocking = False):

        if visited is None:
            visited = set()

        if tile is None or tile.tileCoord in visited:
            return []

        print("FINDING NEXT SIGNAL")
        print("TileLocation")
        print(tile.tileCoord)
        print("Search Direction")
        print(tileDirection)

        visited.add(tile.tileCoord)

        if isinstance(tile, SignalTile):
            if (tile.getDefaultStartDir() == tileDirection):
                print("ReturningTile")
                print(tile.tileCoord)
                return [tile]
        if blocking == False and isinstance(tile,PortalTile):
            return []

        entryDir = (-tileDirection[0], -tileDirection[1])

        coords = tile.getEntryAndExitCoord(entryDir=entryDir,currentStatus=False)

        if isinstance(tile,PointTile) and blocking ==True:
            if tile.isMouth(entryDir):
                pass
                coords = tile.getEntryAndExitCoord(entryDir,True)
            else:
                coords = tile.getEntryAndExitCoord()

        print("directional Coords")
        print(coords)
        print("entry Dir")
        print(entryDir)

        tileList = []
        for coord in coords:
            if coord != entryDir:
                newTileCoordX = tile.tileCoord[0] + coord[1]
                newTileCoordY = tile.tileCoord[1] + coord[0]

                try:#Catching index out of range
                    newTile = self.tileMapper.tileMap[newTileCoordY][newTileCoordX]
                except:
                    return []
                print("Calling Function")
                print("Direction Coord")
                print(coord)
                print("X")
                print(newTileCoordX)
                print("Y")
                print(newTileCoordY)
                result = self.findNextSignal(newTile, coord, visited=visited, blocking=blocking)
                #result = []
                for i in result:
                    tileList.append(i)

        return tileList

    def getSignalList(self,tile, blocking = True):
        print("GETTING SIGNAL LIST")
        print(tile.tileCoord)
        startDir = tile.getDefaultStartDir()
        entryLoc = (startDir[0],startDir[1])
        newTile = self.tileMapper.tileMap[tile.tileCoord[1]+startDir[0]][tile.tileCoord[0]+startDir[1]]
        return self.findNextSignal(newTile,entryLoc, blocking=blocking)