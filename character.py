
class Character:

    def __init__(self):

        self.location = None
        self.current_room = None
        self.attacking = False
        self.facing = (0, -1)
        self.HP = 100
        self.is_alive = True
        self.has_sling = False
        self.has_flippers = False
        self.has_heat_suit = False
        self.has_map = False
        self.wallet = 0


    def set_location(self, column, row, room):

        if room.tiles[column][row].is_empty(): #This allows the movement across lava or water if possible

            if room.tiles[column][row].get_is_fence():

                return None

            elif room.tiles[column][row].get_is_water() and not self.has_flippers:

                return None

            elif room.tiles[column][row].get_is_lava() and not self.has_heat_suit:

                return None

            else:

                self.location = (column, row)
                room.set_character(column, row, self)
                self.current_room = room.get_coordinates()

        else:
            return 0

    def get_location(self):

        return self.location

    def get_type(self):

        return self.type

    def get_facing(self):

        return self.facing

    def set_facing(self, new_facing):

        self.facing = new_facing



    def set_attacking(self,boo):

        self.attacking = boo

    def get_attacking(self):


        return self.attacking

    def set_is_alive(self,boo):

        self.is_alive = boo

    def get_is_alive(self):

        return self.is_alive

    def get_current_room(self):

        return self.current_room

    def add_to_wallet(self, amount):

        self.wallet = self.wallet + amount

    def get_wallet(self):

        return self.wallet


