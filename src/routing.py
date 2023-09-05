from extra import WarningBox
from tileBase import *


class AbstractTrackSection:
    def __init__(self,firstTile,secondTile,tileMapper):
        self.firstTile = firstTile
        self.secondTile = secondTile
        self.tileMapper = tileMapper
        self.active = True
        self.tileList = []

        print(firstTile)
        print(firstTile.tileCoord)
        print(secondTile)
        print(secondTile.tileCoord)
        if not isinstance(firstTile, SignalTile) or not isinstance(secondTile,SignalTile):
            self.active = False
            print("Cann ot auto Track")
            WarningBox("The first and last tiles are not signals","Cannot complete").exec_()
            
            
            
        
    def deleteIfSelected(self,selectedTile):
        for tile in self.tileList:
            if tile==selectedTile:
                self.delete()

    def delete(self):
        print("Deleting")
        self.active = False
        for tile in self.tileList:
            tile.changeColor((255,255,255))
            if isinstance(tile, SignalTile):
                tile.lock =False
                tile.setSignal("Red")
        self.tileList = []
        self.tileMapper.updateSignals()

class AutoTrack(AbstractTrackSection):
    def __init__(self,firstTile,secondTile,tileMapper):
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
                    return
                
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

        for tile in self.tileList:
            tile.changeColor((0,255,255))
            if isinstance(tile,SignalTile):
                tile.setSignal("Green", "Router")
                tile.lock = True

        secondTile.setSignal("Red","Router")
        secondTile.lock = False

        tileMapper.updateSignals()

class BranchSignalTile:
    def __init__(self,tileMapper):
        self.tileMapper = tileMapper

    def findNextSignal(self, tile, tileDirection, visited=None, backLook = True):

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
            if (tile.getDefaultStartDir() == tileDirection and backLook) or not backLook:
                print("ReturningTile")
                print(tile.tileCoord)
                return [tile]

        entryDir = (-tileDirection[0], -tileDirection[1])
        coords = tile.getEntryAndExitCoord(entryDir,False)

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
                result = self.findNextSignal(newTile, coord, visited=visited, backLook=backLook)
                #result = []
                for i in result:
                    tileList.append(i)

        return tileList


    def getSignalList(self,tile, backLook = True):
        startDir = tile.getDefaultStartDir()
        entryLoc = (startDir[0],startDir[1])
        newTile = self.tileMapper.tileMap[tile.tileCoord[1]+startDir[0]][tile.tileCoord[0]+startDir[1]]
        return self.findNextSignal(newTile,entryLoc, backLook=backLook)

class RoutingTrack(AbstractTrackSection,BranchSignalTile):
    def __init__(self,firstTile,secondTile,tileMapper):
        AbstractTrackSection.__init__(self,firstTile,secondTile,tileMapper)


        pathList = self.findSignalPath(firstTile,secondTile)


        pathListTemp = pathList
        pathList = []
        for item in pathListTemp:
            if item not in pathList:
                pathList.append(item)


        print(pathList)

        for i in range(len(pathList)):
            tile = pathList[i]
            tile.changeColor((0,0,255))
            print(tile.tileCoord)

            if isinstance(tile, PointTile):
                nextTile = pathList[i+1]
                prevTile = pathList[i-1]

                nextTileOffset = (nextTile.tileCoord[0]-tile.tileCoord[0],nextTile.tileCoord[1]-tile.tileCoord[1])
                prevTileOffset = (prevTile.tileCoord[0]-tile.tileCoord[0],prevTile.tileCoord[1]-tile.tileCoord[1])

                straightCoord = tile.getEntryAndExitCoord(currentStatus=True,diverge=False)
                curveCoord = tile.getEntryAndExitCoord(currentStatus=True,diverge=True)

                straightCoord = (straightCoord[1],straightCoord[0])
                curveCoord = (curveCoord[1],curveCoord[0])

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

        signalList = self.getSignalList(firstTile, backLook=False)
        print(signalList)
        for signal in signalList:
            if signal!=secondTile:
                self.redSignals.append(signal)
                signal.changeColor((0,255,0))



        for redSignal in self.redSignals:
            redSignal.setSignal("Green", "Router")
            redSignal.lock = True


        self.tileMapper.updateSignals()



    def findSignalPath(self,firstSignal,secondSignal):
        startDir = firstSignal.getDefaultStartDir()
        entryLoc = (startDir[0],startDir[1])
        newTile = self.tileMapper.tileMap[firstSignal.tileCoord[1]+startDir[0]][firstSignal.tileCoord[0]+startDir[1]]
        print("FINGING NEXT SIGNAL PATH")
        path = self.findNextSignalPath(newTile,entryLoc, secondSignal)
        path.append(newTile)
        return [firstSignal]+path
    
    def findNextSignalPath(self, tile, tileDirection,targetTile, visited=None):

        if visited is None:
            visited = set()

        if tile is None or tile.tileCoord in visited:
            return None

        # print("FINDING NEXT SIGNAL")
        # print("TileLocation")
        # print(tile.tileCoord)
        # print("Search Direction")
        # print(tileDirection)

        visited.add(tile.tileCoord)

        if isinstance(tile, SignalTile):
            if tile == targetTile:
                print("TILE IS RETURNED")
                print(tile.tileCoord)
                return [tile]

        entryDir = (-tileDirection[0], -tileDirection[1])
        coords = tile.getEntryAndExitCoord(entryDir,False)

        # print("directional Coords")
        # print(coords)
        # print("entry Dir")
        # print(entryDir)

        resultList = []
        for coord in coords:
            if coord != entryDir:
                newTileCoordX = tile.tileCoord[0] + coord[1]
                newTileCoordY = tile.tileCoord[1] + coord[0]

                try:#Catching index out of range
                    newTile = self.tileMapper.tileMap[newTileCoordY][newTileCoordX]
                except:
                    return None
                # print("Calling Function")
                # print("Direction Coord")
                # print(coord)
                # print("X")
                # print(newTileCoordX)
                # print("Y")
                # print(newTileCoordY)

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
                     
                    result.append(tile)
                    return result

        # print("RECURSION CALL")
        # print(tile.tileCoord)
        # print("Trailing")
        # for result in resultList:
        #     if result!=None:
        #         for i in result:
        #             if i!=None:
        #                 print(i.tileCoord)
        #             else:
        #                 print(i)
        #     else:
        #         print(result)


        return None
