
class Tile:

    def __init__(self, y,x, room_size):

        self.tile_location = (y, x)
        self.room_size = room_size
        self.sign = None
        self.character = None
        self.is_wall = False
        self.switch = None
        self.target = None
        self.win_switch = None
        self.is_water = False
        self.is_lava = False
        self.is_door = False
        self.is_stone = False
        self.is_fence = False
        self.container = None
        self.outer_walls = []
        self.outer_walls_for_room_switches()


    def get_location(self):

        return self.tile_location

    def set_sign(self, foo):
        if self.is_empty():
            self.sign = foo
            self.sign.set_location(self.tile_location)
            return True
        else:
            return False

    def is_sign_tile(self):

        if self.sign != None:

            return True
        else:
            return False

    def get_sign(self):

        return self.sign

    def is_wall_tile(self):

        return self.is_wall

    def is_empty(self): #would flag system be better?

        if not self.is_wall and self.character is None and not self.is_door and self.container is None and self.sign is None:

            return True

        else:
            return False

    def set_character(self, character):

        if self.is_empty() and not self.is_water:
            self.character = character
            return True
        else:
            return False

    def get_character(self):

        return self.character

    def clear_character(self):
        if self.character != None:
            self.character = None

    def set_wall(self):

        if self.is_empty():
            self.is_wall = True
            return True
        else:
            return False

    def set_container(self,container):

        if self.is_empty():
            self.container = container
            return True
        else:
            return False

    def is_container_tile(self):

        if self.container != None:

            return True

    def get_container(self):

        return self.container



    def set_door(self,boo):
        if self.is_wall:
            self.is_wall=False
        self.is_door = boo



    def is_door_tile(self):

        return self.is_door


    def get_is_stone(self):

        return self.is_stone

    def set_is_stone(self):

        if not self.get_is_stone() and self.is_empty() and self.get_location() not in self.outer_walls:

            self.is_stone = True

        else:

            self.is_stone = False

    def set_water(self):

        if self.is_empty():
            self.is_water=True
        else:
            pass

    def get_is_lava(self):

        if self.is_lava==True:
            return self.is_lava
        else:
            return False

    def set_lava(self):

        if self.is_empty():
            self.is_lava=True
        else:
            pass

    def get_is_fence(self):

        if self.is_fence==True:
            return self.is_fence
        else:
            return False

    def set_fence(self):

        if self.is_empty():
            self.is_fence=True
        else:
            pass


    def get_is_water(self):

        if self.is_water==True:
            return self.is_water
        else:
            return False

    def set_switch(self,switch):

        if self.is_empty():
            self.switch = switch
            return True
        else:
            return False

    def is_switch_tile(self):

        if self.switch != None:

            return True

    def get_switch(self):

        return self.switch

    def set_win_switch(self, win_switch):

        if self.is_empty():
            self.win_switch = win_switch
            return True
        else:
            return False

    def is_win_switch_tile(self):

        if self.win_switch != None:
            return True

    def get_win_switch(self):

        return self.win_switch

    def set_target(self,target):

        if self.is_empty():
            self.target = target
            return True
        else:
            return False

    def is_target_tile(self):

        if self.target != None:

            return True

    def get_target(self):

        return self.target

    def outer_walls_for_room_switches(self):

        side=self.room_size
        for i in range(side):
            for k in range(side):
                if i == 0 or i == side - 1 or k == 0 or k == side - 1:
                    self.outer_walls.append((i, k))

        return self.outer_walls

    def get_outer_walls(self):

        return self.outer_walls

