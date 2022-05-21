from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.Qt import QPixmap


class SwitchGraphics(QGraphicsPixmapItem):



    def __init__(self, type):

        super().__init__()

        self.type = type  # Determines which type of item is drawn

        self.set_image()

    def set_image(self):
        """
        Sets the correct Pixmap-image depending on the type.
        """

        if self.type == 0:
            self.setPixmap(QPixmap('images/button_on.png'))

        elif self.type == 1:
            self.setPixmap(QPixmap('images/button_off.png'))

        elif self.type == 2:

            self.setPixmap(QPixmap('images/win_switch.png'))

