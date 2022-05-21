from character import Character
from weapon import Weapon

class Player(Character):

    def __init__(self):
        super().__init__()
        self.type = "player"
        self.has_key = False
        self.weapon = Weapon("basic sword", 20)
        self.armour = None
        self.inventory = []
        self.add_to_inventory(self.weapon)



    def add_to_inventory(self, item_to_add):
        self.inventory.append(item_to_add)

    def get_inventory(self):
        return self.inventory

    def set_key(self, boo):

        j=0
        if boo==False:
            # The below stricture was added for multiple keys, prior use of set_key() in GUI was set up for player having one key at a time
            # this allows for player to have more than one key without large amounts of changes to GUI code.
            for i in self.inventory:

                if i.get_name() == 'key' and j==0:
                    self.has_key=False
                    j+=1
                elif i.get_name() == 'key' and j >0:
                    self.has_key = True
                    j += 1
        else:
            self.has_key=boo







    def get_has_key(self):
        return self.has_key

    def set_armour(self, armour):

        self.armour = armour

    def set_flippers(self):

        self.has_flippers=True

    def set_heat_suit(self):

        self.has_heat_suit = True

    def get_has_heat_suit(self):

        return self.has_heat_suit


    def set_has_sling(self):

        self.has_sling=True

    def get_has_sling(self):

        return self.has_sling

    def set_has_map(self):

        self.has_map=True

    def get_has_map(self):

        return self.has_map

    def get_has_flippers(self):

        return self.has_flippers

    def get_character_type(self):

        return self.type

    def remove_from_inventory(self, name):

        for x in self.inventory: #need individual names for items otherwise shared named items will all be deleted
            if x.get_name()==name:
                self.inventory.remove(x)



