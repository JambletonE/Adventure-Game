class Item:

    def __init__(self, item_type):

        self.item_type = item_type
        self.name = item_type

    def get_type(self):

        return self.item_type

    def get_name(self):

        return self.name

