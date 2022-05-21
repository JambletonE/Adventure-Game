from item import Item

class Coin(Item):

    def __init__(self,item_type,value):
        super().__init__(item_type)
        self.value = value

    def get_value(self):

         return self.value



