from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap

class AttackGraphics(QGraphicsPixmapItem):

    def __init__(self, character, tile_size):
        super().__init__()

        self.set_image()
        self.rot_angle=None
        self.character = character
        self.tile_size = tile_size
        #self.updatePosition()
        self.updateRotation()



    def set_image(self):

        self.setPixmap(QPixmap('images/sword_2.png'))





    """
        def updatePosition(self):

        print("hi")
        p = self.character.get_location()
        self.setPos(p[0]*self.tile_size, p[1]*self.tile_size)
        print("hi2")
    
    """




    def updateRotation(self):

        rot_direc = self.character.get_facing()

        rot_angle=0
        if rot_direc == (0, -1):
            self.rot_angle = 0
        if rot_direc == (0, 1):#down
            self.rot_angle = 180
        if rot_direc == (-1, 0):
            self.rot_angle = 270
        if rot_direc == (1, 0):#right
            self.rot_angle = 90 #

        self.setRotation(self.rot_angle)

    def get_rot_angle(self):

        return self.rot_angle
