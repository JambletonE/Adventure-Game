from character import Character

class Enemy(Character):


    def __init__(self,power):
        super().__init__()
        self.power = power
        self.type = "enemy"

    def get_power(self):

        return self.power

    def get_character_type(self):

        return self.type
