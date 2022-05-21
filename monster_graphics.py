from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap


class MonsterGraphics(QGraphicsPixmapItem):
    """
    This class handles drawing of the items.
    """

    def __init__(self):
        super().__init__()

        self.set_image()

    def set_image(self):
        self.setPixmap(QPixmap('images/monster.png'))
