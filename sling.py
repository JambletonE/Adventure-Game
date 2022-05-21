from item import Item

class Sling(Item):

    def __init__(self,item_type):
        super().__init__(item_type)
        self.level = 0

    def get_level(self):

         return self.level

