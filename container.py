class Container(object):

    def __init__(self):

        self.type = "chest"
        self.item = None
        self.location = None
        self.is_full = True

    def set_item(self,item):

        self.item=item

    def get_item(self):

        return self.item

    def set_location(self, column, row, room):#
        if room.tiles[column][row].is_empty():
            self.location=(column, row)
            room.set_container(column, row, self)

    def get_location(self):

        return self.location

    def set_is_full(self,boo):

        self.is_full = boo

    def get_is_full(self):

        return self.is_full








