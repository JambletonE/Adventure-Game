from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap
from random import randrange

class DoorGraphics(QGraphicsPixmapItem):


    def __init__(self):
        super().__init__()

        self.set_image()

    def set_image(self):

            self.setPixmap(QPixmap('images/door.png'))

