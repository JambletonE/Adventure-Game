
from tile import Tile

class Room:

    #tiles: list[list[int]]

    def __init__(self, room_size,coordinates):


        self.room_size = room_size
        self.room_coordinates= coordinates
        self.tiles = [[1 for i in range(self.room_size)] for j in range(self.room_size)]
        self.player_last_pos=None
        self.player_last_facing=None
        for i in range(self.room_size):
            for k in range(self.room_size):
                self.tiles[i][k] = Tile(i, k, self.room_size)


        for i in range(self.room_size): ##setting outer walls
            self.tiles[0][i].set_wall()
            self.tiles[i][0].set_wall()
            self.tiles[i][self.room_size-1].set_wall()
            self.tiles[self.room_size-1][i].set_wall()

        self.characters_in_room = []
        self.containers_in_room = []
        self.switches_in_room = []
        self.win_switches_in_room=[]
        self.targets_in_room = []


    def set_character(self,column,row,character):

        self.tiles[column][row].set_character(character)
        if character not in self.characters_in_room:
            self.characters_in_room.append(character)


    def get_coordinates(self):

        return self.room_coordinates

    def get_characters_in_room(self):

        return self.characters_in_room

    def print_room(self):

        for x in self.tiles:
            print(x)

    def set_container(self,column,row,container):

        if self.tiles[column][row].is_empty():
            self.tiles[column][row].set_container(container)
            self.containers_in_room.append(container)
        else:
            pass

    def set_switch(self,column,row,switch):

        if self.tiles[column][row].is_empty():
            self.tiles[column][row].set_switch(switch)
            self.switches_in_room.append(switch)
        else:
            pass

    def set_win_switch(self,column,row,win_switch):

        if self.tiles[column][row].is_empty():
            self.tiles[column][row].set_win_switch(win_switch)
            self.switches_in_room.append(win_switch)
        else:
            pass

    def get_win_switches_in_room(self):

        return self.win_switches_in_room

    def get_switches_in_room(self):

        return self.switches_in_room

    def get_room_size(self):

        return self.room_size


    def get_player_last_pos(self):##############Delete

        return self.player_last_pos

    def get_player_last_facing(self):

        return self.player_last_facing

    def set_player_last_pos(self, pos):

        self.player_last_pos = pos

    def set_player_last_facing(self, facing):

        self.player_last_facing = facing

    def all_switches_are_on(self):

        if len(self.switches_in_room)>0:
            for x in self.switches_in_room:
                if not x.get_is_on():
                    return False

            return True

        else:
            return False

    def all_targets_are_hit(self):

        if len(self.targets_in_room)>0:
            for x in self.targets_in_room:
                if not x.get_is_on():
                    return False

            return True

        else:
            return False

    def set_target(self,column,row,target):

        if self.tiles[column][row].is_empty():
            self.tiles[column][row].set_target(target)
            self.targets_in_room.append(target)
        else:
            pass

    def get_win_targets_in_room(self):

        return self.targets_in_room



