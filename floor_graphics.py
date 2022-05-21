from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap
from random import randrange

class FloorGraphics(QGraphicsPixmapItem):

    def __init__(self, rn2):
        super().__init__()

        self.set_image(rn2)

    def set_image(self,rn2):


        if rn2==0:
            self.setPixmap(QPixmap('images/water_1.png'))


        elif rn2==1:
            self.setPixmap(QPixmap('images/water_2.png'))

        elif rn2==2:
            self.setPixmap(QPixmap('images/water_3.png'))

        elif rn2==3:
            self.setPixmap(QPixmap('images/water_4.png'))

        elif rn2==5:
            self.setPixmap(QPixmap('images/water_5.png'))

        else:
            self.setPixmap(QPixmap('images/water_6.png'))
