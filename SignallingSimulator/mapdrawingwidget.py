from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen,QImage ,QColor, QFont, QPolygon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect, QPoint
from extra import ReplacableImage

ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR

class MapDrawingWidget(QWidget):
    mousePressSignal = pyqtSignal(int, int)


    def __init__(self, parent):
        super().__init__(parent)
        # self.rect_x = 50
        # self.rect_y = 100
        # self.rect_width = 300
        # self.rect_height = 100
        # self.direction = 1

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_position)
        # self.timer.start(20)  # Update every 20 milliseconds

        size = self.size()
        self.width, self.height = size.width(), size.height()

        self.last_mouse_pos = None
        self.dy = 0
        self.dx = 0
        # self.camera_x, self.camera_y = 0, 0

        # self.camera_x_min = -40  # Set the minimum X coordinate limit
        # self.camera_x_max = 40   # Set the maximum X coordinate limit
        # self.camera_y_min = -40  # Set the minimum Y coordinate limit
        # self.camera_y_max = 40   # Set the maximum Y coordinate limit

        # self.camera_scale = 1

        # self.left   = 0
        # self.right  = self.width
        # self.bottom = 0
        # self.top    = self.height
        # self.zoom_level = 1
        # self.zoomed_width  = self.width
        # self.zoomed_height = self.height
        self.center_x = 0
        self.center_y = 0
        self.zoom_level =1

        self.train_list = {}
        self.tile_list = []
        self.train_to_del = None

        self.select_pos = [0,0]
        self.select_visible = False

        # self.draw_train((0,0),"1k45")
        # self.draw_train((100,50),"1r56")

        # self.del_train("1k45")

        self.textData = None

        self.cur_font = self.font()

        # trackA = ReplacableImage('assets/trackRedSignal.png')
        # trackB = ReplacableImage('assets/trackRedSignal.png')

        # trackA.flip = True
        # trackB.flip = False

        # trackA.point = 0
        # trackB.point = 0

        # self.draw_tile((200,50),trackA)
        # self.draw_tile((200,100),trackB)

    def update_position(self):
        # Update the x position of the rectangle
        self.rect_x += self.direction * 5

        # Check boundaries and reverse direction if necessary
        if self.rect_x + self.rect_width > self.width() or self.rect_x < 0:
            self.direction *= -1

        # Trigger a repaint
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_background(painter)
        self.draw_all(painter)
    
    def draw_background(self, painter):
        # Draw the black background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawRect(self.rect())

    def zoomToPoint(self,point):
        print("ZOOM TO POINT")
        print(self.width)
        print(self.height)
        print(point)
        self.zoom_level = 1
        self.center_x = point[0] - (self.width * self.zoom_level *6 )
        self.center_y = point[1] + (self.height * self.zoom_level *6 )
        self.update()

    def translate_distance(self,x,y, width, height):

        x = int((x - self.center_x)/self.zoom_level)
        y = -int((y - self.center_y)/self.zoom_level)


        width = int(width / self.zoom_level)
        height = int(height / self.zoom_level)

        return x,y,width, height

    
    def draw_train(self, pos, text, entryModel, forwardDir):#Text has to be unique
        self.train_list[text] = (pos, entryModel, forwardDir)
        self.update()

    def del_all_train(self):
        print("Del All train")
        self.train_list = {}
        self.update()

    def del_train(self,text):
        self.train_list = {}
        self.train_to_del = text
        self.update()

    def del_all_tile(self):
        self.tile_list = []
        self.update()

    def draw_tile(self, pos,image):

        for tile in self.tile_list:
            if tile[1] == pos: #Tile already exists
                self.tile_list.remove(tile)

        self.tile_list.append((image,pos))
        self.update()
    

    def setText(self, textData):
        self.textData = textData

    def draw_all(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)


        for item in self.tile_list:
            tile = item[0]
            pos = item[1]
            x,y,width,height = self.translate_distance(pos[0],pos[1],50,50)

            tile.draw_tile(painter, x,y,width)
            # image = image.render()
            # target_rect = QRect(x, y, width, height)
            # painter.drawImage(target_rect, image)

        if self.train_to_del != None:
            self.train_list.pop(self.train_to_del)
            self.train_to_del = None

        for text, trainData in self.train_list.items():
            pos = trainData[0]
            style = trainData[1]
            forwardDir = trainData[2]
            if pos is not None:
                x, y, width, height = self.translate_distance(pos[0], pos[1], 50, 20)
                x=int(x)
                y=int(y)

                if style:
                    # Draw the green circle
                    radius = min(width, height) // 1  # Choose an appropriate radius
                    center_x = x + width // 2
                    center_y = y + height // 2
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                    painter.drawEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
                    text_color = Qt.black
                else:
                    # Draw the rectangle
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                    painter.drawRect(x, y, width, height)
                    text_color = Qt.white

                    # Draw the blue arrow
                    arrow_size = int(10 //self.zoom_level)  # Size of the arrow
                    if forwardDir is not None:
                        if forwardDir==True:
                            # Draw arrow on the left
                            arrow_x = x - arrow_size
                            arrow_points = [
                                QPoint(arrow_x, y + height // 2),
                                QPoint(arrow_x + arrow_size, y + height // 2 - arrow_size // 2),
                                QPoint(arrow_x + arrow_size, y + height // 2 + arrow_size // 2)
                            ]
                        elif forwardDir==False:
                            # Draw arrow on the right
                            arrow_x = x + width
                            arrow_points = [
                                QPoint(arrow_x, y + height // 2),
                                QPoint(arrow_x - arrow_size, y + height // 2 - arrow_size // 2),
                                QPoint(arrow_x - arrow_size, y + height // 2 + arrow_size // 2)
                            ]

                        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
                        painter.drawPolygon(QPolygon(arrow_points))

                # Draw the text centered in the shape
                painter.setPen(QPen(text_color))
                painter.setFont(self.cur_font)
                text_rect = painter.boundingRect(x, y, width, height, Qt.AlignCenter, text)
                painter.drawText(text_rect, Qt.AlignCenter, text)

        #Draw text
        if self.textData!=None:
            font = QFont('Arial', int(14/ self.zoom_level))
            painter.setFont(font)
            pen = QPen(Qt.white)
            painter.setPen(pen)

            # These values are hardcoded in alot of places **BAD**
            row_height = 50
            column_width = 50
        
            for item in self.textData:
                row = item['row']
                column = item['column']
                text = item['text']
 
                x = row * column_width
                y = column * row_height  # Adding 5 to row to handle negative rows
                x,y,width,height = self.translate_distance(x,y,50,50)
                painter.drawText(x, y, text)


        if self.select_visible:
            x,y,width,height = self.translate_distance(self.select_pos[0],self.select_pos[1],50,50)
            target_rect = QRect(x, y, width, height)
            pen = QPen(QColor(128, 0, 128), 5, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(target_rect)

        # x,y,width,height = self.translate_distance(self.rect_x,self.rect_y,self.rect_width,self.rect_height)

        # # Draw the rectangle
        # painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        # painter.drawRect(x,y,width,height)

        # # Draw the text centered in the rectangle
        # text = "Hello, QPainter!"
        # painter.setPen(QPen(Qt.white))
        # painter.setFont(self.font())
        # text_rect = painter.boundingRect(x,y,width,height, Qt.AlignCenter, text)
        # painter.drawText(text_rect, Qt.AlignCenter, text)



    def mouseMoveEvent(self, event):
        # Handle mouse movement and update camera position
        if event.buttons() == Qt.LeftButton:
            current_pos = event.pos()
            if self.last_mouse_pos is None:
                self.last_mouse_pos = current_pos
            dx = (current_pos.x() - self.last_mouse_pos.x())
            dy = -(current_pos.y() - self.last_mouse_pos.y())

            self.center_x -= dx*(self.zoom_level*1)
            self.center_y -= dy*(self.zoom_level*1)

            self.last_mouse_pos = current_pos
        self.update()

            
    def mouseReleaseEvent(self, event):
        # Reset last mouse position when the mouse button is released
        self.last_mouse_pos = None

    def wheelEvent(self,event):
        f = ZOOM_OUT_FACTOR if event.angleDelta().y() > 0 else ZOOM_IN_FACTOR if event.angleDelta().y() < 0 else 1
        self.zoomScreen(f)

    def zoomScreen(self,f):

        self.cur_font.setPointSize(int((1/self.zoom_level)*10))

        self.zoom_level *= f
        self.update()

    # def zoomScreen(self, f,x,y):
    #     # If zoom_level is in the proper range
    #     if .2 < self.zoom_level*f < 5:
    #         self.zoom_level *= f

    #         mouse_x = x/self.width
    #         mouse_y = y/self.height

    #         mouse_x_in_world = self.left   + mouse_x*self.zoomed_width
    #         mouse_y_in_world = self.bottom + mouse_y*self.zoomed_height

    #         self.zoomed_width  *= f
    #         self.zoomed_height *= f

    #         self.left   = mouse_x_in_world - mouse_x*self.zoomed_width
    #         self.right  = mouse_x_in_world + (1 - mouse_x)*self.zoomed_width
    #         self.bottom = mouse_y_in_world - mouse_y*self.zoomed_height
    #         self.top    = mouse_y_in_world + (1 - mouse_y)*self.zoomed_height

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()

            mapX = int((self.zoom_level*x)+ self.center_x)
            mapY = int((self.zoom_level*-y)+ self.center_y)


            self.mousePressSignal.emit(mapX, mapY)  # Emit the signal with x and y coordinates

    def zoomToActualSize(self,tilemap):
        if tilemap!= None:
            # zoomHeightOld = self.zoomed_height
            # prop = self.zoomed_width / self.zoomed_height

            # if tilemap.width>tilemap.height:
            #     self.zoomed_width = tilemap.width*50
            #     self.zoomed_height = self.zoomed_width /prop
            # else:
            #     self.zoomed_height = tilemap.height*50
            #     self.zoomed_width = self.zoomed_height * prop

            # self.left = 0
            # self.bottom = 0
            # self.right = self.zoomed_width
            # self.top = self.zoomed_height

            # x = int((x - self.center_x)/self.zoom_level)
            # y = -int((y - self.center_y)/self.zoom_level)


            # width = int(width / self.zoom_level)
            # height = int(height / self.zoom_level)

            self.center_x = 0
            self.center_y = 200
            self.zoom_level = 1
            self.repaint()

            # self.zoom_level = self.zoom_level * (self.zoomed_height/zoomHeightOld)