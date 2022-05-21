from PyQt5 import QtWidgets, QtGui, QtCore


class CharacterGraphicsItem(QtWidgets.QGraphicsPolygonItem):


    def __init__(self, character, tile_size):

        super(CharacterGraphicsItem, self).__init__()

        self.character = character
        self.tile_size = tile_size
        self.setBrush(QtGui.QBrush(4))
        self.constructPentagonVertices()
        self.updateAll()



    def constructPentagonVertices(self):
       
        # Create a new QPolygon object
        pentagon = QtGui.QPolygonF()

        # Add the corners of a triangle to the polygon object
        pentagon.append(QtCore.QPointF(self.tile_size/2, 0)) # Tip
        pentagon.append(QtCore.QPointF(2, self.tile_size/2))#Top Left (when pointing up)
        pentagon.append(QtCore.QPointF(2, self.tile_size-2))#Bottom left
        pentagon.append(QtCore.QPointF(self.tile_size - 2, self.tile_size- 2))  # Bottom Right
        pentagon.append(QtCore.QPointF(self.tile_size-2, self.tile_size/2))#Top right

        pentagon.append(QtCore.QPointF(self.tile_size/2, 0)) # Tip


        self.setPolygon(pentagon)


        self.setTransformOriginPoint(self.tile_size/2, self.tile_size/2)

    def updateAll(self):

        self.updatePosition()
        self.updateRotation()
        self.updateColor()


    def updatePosition(self):

        p=self.character.get_location()
        self.setPos(p[0]*self.tile_size,p[1]*self.tile_size)



    def updateRotation(self):

        rot_direc = self.character.get_facing()

        rot_angle=0
        if rot_direc == (0, -1):
            rot_angle = 0
        if rot_direc == (0, 1):#down
            rot_angle = 180
        if rot_direc == (-1, 0):
            rot_angle = 270
        if rot_direc == (1, 0):#right
            rot_angle = 90 #

        self.setRotation(rot_angle)



    def updateColor(self):

        if self.character.is_alive:
            self.setBrush(QtGui.QColor(255, 255, 0))
        else:
            self.setBrush(QtGui.QColor(255, 0, 0))










