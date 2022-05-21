
class RoomArray:

    def __init__(self, size):

        self.size=size
        self.room_array = [[None] * size for i in range(size)]


    def get_array(self):

        return self.room_array


    def add_room(self, room_to_add):

        coords = room_to_add.get_coordinates()
        self.room_array[coords[0]][coords[1]] = room_to_add

    def get_room(self, coords):

        return self.room_array[coords[0]][coords[1]]


    def get_adjacent_room(self,room, direction):

        original_coords = list(room.get_coordinates())
        adjacent_room_coords = list((None, None))
        adjacent_room_coords[0] = original_coords[0] + direction[0]
        adjacent_room_coords[1] = original_coords[1] + direction[1]
        adjacent_room_coords = tuple(adjacent_room_coords)

        return adjacent_room_coords


