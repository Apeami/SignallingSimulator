from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect
import math

class DrawMapTile:
    def __init__(self, flip, point, tileType, color):
        self.flip = flip
        self.point = point
        self.tileType = tileType
        self.color = color

    def draw_straight(self,x,y, width, painter):
        half = width//2
        pen = QPen(self.color, width/10, Qt.SolidLine)
        painter.setPen(pen)
        if self.point =='east' or self.point =='west':
            start_point = QPoint(x - half, y)
            end_point = QPoint(x + half, y)
            painter.drawLine(start_point, end_point)
        if self.point =='north' or self.point == 'south':
            start_point = QPoint(x , y - half)
            end_point = QPoint(x , y + half)
            painter.drawLine(start_point, end_point)

    def draw_curve(self,x,y,width, painter):
        half = width//2
        diawidth = int(math.sqrt(2*half*half)/1.4)
        midPoint = QPoint(x,y)
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self.color, width/10, Qt.SolidLine)
        painter.setPen(pen)
        if self.point=="east":
            firstPoint = QPoint(x - half, y)
            if self.flip == True:                    
                endPoint = QPoint(x + diawidth, y + diawidth)
            if self.flip == False:                    \
                endPoint = QPoint(x + diawidth, y - diawidth)
        if self.point=="west":
            firstPoint = QPoint(x + half, y)
            if self.flip == True:                    
                endPoint = QPoint(x - diawidth, y - diawidth)
            if self.flip == False:                    
                endPoint = QPoint(x - diawidth, y + diawidth)
        if self.point=="south":
            firstPoint = QPoint(x, y - half)
            if self.flip == False:                    
                endPoint = QPoint(x + diawidth, y + diawidth)
            if self.flip == True:                    
                endPoint = QPoint(x - diawidth, y + diawidth)
        if self.point=="north":
            firstPoint = QPoint(x, y + half)
            if self.flip == False:                    
                endPoint = QPoint(x - diawidth, y - diawidth)
            if self.flip == True:                    
                endPoint = QPoint(x + diawidth, y - diawidth)

        path = QPainterPath()
        path.moveTo(firstPoint)
        path.quadTo(midPoint, endPoint)
                
        painter.drawPath(path)


    def draw_tile(self, painter,x,y,width):

        half = width//2
        x+=half
        y+=half
        diawidth = int(math.sqrt(2*half*half)/1.4)

        if self.tileType == "RedSignal" or self.tileType == "YellowSignal" or self.tileType == "DYellowSignal" or self.tileType == "GreenSignal":
            self.draw_straight(x,y,width, painter)
            painter.setBrush(QBrush(QColor(255, 0, 0)))  # Set brush to red color
            painter.setPen(Qt.NoPen)
            
            if self.point == 'east':
                painter.setPen(QPen(Qt.white, width/20, Qt.SolidLine))
                start_point = QPoint(x - half//2, y)
                end_point = QPoint(x - half//2, y - half*10//16)
                painter.drawLine(start_point, end_point)
                start_point = end_point
                end_point = QPoint(x + half//4, y - half*10//16)
                painter.drawLine(start_point, end_point)

                self.setBrushSignal(painter) 
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(x + half//4, y - half*10//16), width//8, width//8)

            if self.point == 'west':
                painter.setPen(QPen(Qt.white, width/20, Qt.SolidLine))
                start_point = QPoint(x + half//2, y)
                end_point = QPoint(x + half//2, y + half*10//16)
                painter.drawLine(start_point, end_point)
                start_point = end_point
                end_point = QPoint(x - half//4, y + half*10//16)
                painter.drawLine(start_point, end_point)

                self.setBrushSignal(painter)  
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(x - half//4, y + half*10//16), width//8, width//8)

            if self.point == 'north':
                pass

            if self.point == 'south':
                pass

        elif self.tileType == "Straight":
            self.draw_straight(x,y,width, painter)

        elif self.tileType == "Diagonal":
            pen = QPen(self.color, width/10, Qt.SolidLine)
            painter.setPen(pen)
            if self.point =='west':
                diawidth = int(math.sqrt(2*half*half)/1.4)
                start_point = QPoint(x - diawidth, y- diawidth)
                end_point = QPoint(x + diawidth, y + diawidth)
                painter.drawLine(start_point, end_point)
            if self.point =='east':
                diawidth = int(math.sqrt(2*half*half)/1.4)
                start_point = QPoint(x + diawidth, y- diawidth)
                end_point = QPoint(x - diawidth, y + diawidth)
                painter.drawLine(start_point, end_point)

        elif self.tileType== "Platform":
            self.draw_straight(x,y,width, painter)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 192, 203)))
            if self.point =='east' or self.point =='west':
                if self.flip == False:
                    rect = QRect(x - half,y + half//10, 2*half, half*9//10)
                    painter.drawRect(rect)
                if self.flip == True:
                    rect = QRect(x - half,y - half, 2*half, half*9//10)
                    painter.drawRect(rect)
            if self.point =='north' or self.point == 'south':
                pass #TODO



        elif self.tileType == "PointOpen":
            pen = QPen(self.color, width/10, Qt.SolidLine)
            painter.setPen(pen)
            self.draw_straight(x,y,width, painter)
            if (self.point == 'east' and self.flip ==False) or (self.point =='north' and self.flip == True):
                start_point = QPoint(x + diawidth//2, y - diawidth//2)
                end_point = QPoint(x + diawidth, y - diawidth)
                painter.drawLine(start_point, end_point)

            if (self.point == 'west' and self.flip ==False) or (self.point =='south' and self.flip == True):
                start_point = QPoint(x - diawidth//2, y + diawidth//2)
                end_point = QPoint(x - diawidth, y + diawidth)
                painter.drawLine(start_point, end_point)

            if (self.point == 'north' and self.flip ==False) or (self.point =='west' and self.flip == True):
                start_point = QPoint(x - diawidth//2, y - diawidth//2)
                end_point = QPoint(x - diawidth, y - diawidth)
                painter.drawLine(start_point, end_point)

            if (self.point == 'south' and self.flip ==False) or (self.point =='east' and self.flip == True):
                start_point = QPoint(x + diawidth//2, y + diawidth//2)
                end_point = QPoint(x + diawidth, y + diawidth)
                painter.drawLine(start_point, end_point)
        
        elif self.tileType == "PointClose":
            pen = QPen(self.color, width/10, Qt.SolidLine)
            painter.setPen(pen)
            self.draw_curve(x,y,width, painter)
            if self.point == 'east':
                start_point = QPoint(x + half//2, y )
                end_point = QPoint(x + half, y)
                painter.drawLine(start_point, end_point)
            if self.point == 'west':
                start_point = QPoint(x - half//2, y )
                end_point = QPoint(x - half, y)
                painter.drawLine(start_point, end_point)
            if self.point == 'south':
                start_point = QPoint(x , y + half//2)
                end_point = QPoint(x, y + half)
                painter.drawLine(start_point, end_point)
            if self.point == 'north':
                start_point = QPoint(x, y - half//2 )
                end_point = QPoint(x, y - half)
                painter.drawLine(start_point, end_point)

        elif self.tileType == "Buffer":
            pass #TODO

        elif self.tileType == "Continuation":
            self.draw_straight(x,y,width, painter)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(0, 0, 255)))
            if self.point =='west':
                rect = QRect(x-half,y-half, half, half*2)
                painter.drawRect(rect)
            if self.point =='north':#TODO
                rect = QRect(x-half,y-half, half*2, half)
                painter.drawRect(rect)
            if self.point =='east':
                rect = QRect(x,y-half, half, half*2)
                painter.drawRect(rect)
            if self.point == 'south':#TODO
                rect = QRect(x-half,y, half*2, half)
                painter.drawRect(rect)

        elif self.tileType == "Curve":
            self.draw_curve(x,y,width, painter)



        else:
            print("No definition")

    def setBrushSignal(self, painter):
        if self.tileType == "RedSignal":
            painter.setBrush(QBrush(QColor(255, 0, 0)))
        if self.tileType == "YellowSignal":
            painter.setBrush(QBrush(QColor(255, 255, 0)))
        if self.tileType == "DYellowSignal":
            painter.setBrush(QBrush(QColor(255, 255, 0)))
        if self.tileType == "GreenSignal":
            painter.setBrush(QBrush(QColor(0, 254, 0)))