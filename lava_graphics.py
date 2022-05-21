from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap
from random import randrange

class LavaGraphics(QGraphicsPixmapItem):

    def __init__(self, rn2):
        super().__init__()

        self.set_image(rn2)

    def set_image(self,rn2):


        if rn2==0:
            self.setPixmap(QPixmap('images/lava1.png'))


        elif rn2==1:
            self.setPixmap(QPixmap('images/lava2.png'))

        elif rn2==2:
            self.setPixmap(QPixmap('images/lava3.png'))

        elif rn2==3:
            self.setPixmap(QPixmap('images/lava4.png'))

        elif rn2==5:
            self.setPixmap(QPixmap('images/lava5.png'))

        else:
            self.setPixmap(QPixmap('images/lava6.png'))
