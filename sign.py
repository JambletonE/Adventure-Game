
from PyQt5.Qt import QGraphicsPixmapItem
from PyQt5.QtWidgets import  QMessageBox

class Sign(object):

    def __init__(self, message):

        self.name="sign"
        self.message=message
        self.location=None




    def get_message(self):

        return self.message

    def set_location(self,foo):

        self.location=foo

    def get_location(self):

        return self.location

    def init_sign(self):

       sign = QMessageBox()

       sign.setIconPixmap(QGraphicsPixmapItem.QPixmap("sign.png"))
       sign.setWindowTitle("Sign")
       sign.setText(self.message)
       sign.exec_()



