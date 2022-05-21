from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap


class WallGraphics(QGraphicsPixmapItem):

    def __init__(self, rn2):
        super().__init__()

        self.set_image(rn2)

    def set_image(self,rn2):


        if rn2==0:
            self.setPixmap(QPixmap('images/wall_1.png'))

        elif rn2==1:
            self.setPixmap(QPixmap('images/wall_2.png'))

        elif rn2==2:
            self.setPixmap(QPixmap('images/wall_3.png'))

        else:
            self.setPixmap(QPixmap('images/wall_4.png'))
