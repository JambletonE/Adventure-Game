from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap
from random import randrange

class FenceGraphics(QGraphicsPixmapItem):

    def __init__(self, rn2):
        super().__init__()

        self.set_image(rn2)

    def set_image(self,rn2):


        if rn2==0:
            self.setPixmap(QPixmap('images/fence.png'))


        "......more to come maybe"
