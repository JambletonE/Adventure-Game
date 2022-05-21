
class Weapon:

    def __init__(self,name,power):

        self.item_type = "weapon"###
        self.name = name
        self.power = power

    def get_name(self):

        return self.name

    def get_power(self):

        return self.power
