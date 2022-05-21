import unittest
from gui import GUI
from tile import Tile
from room import Room
from room_array import RoomArray
from player import Player



class TestingAdventure(unittest.TestCase):

    def testing_distance_func(self):

        self.assertEqual(GUI.calculate_distance(self, (12,11),(11,11)),1)
        self.assertNotEqual(GUI.calculate_distance(self, (10, 20), (10, 10)), 1)

    def test_opposite_door(self):

        self.room_size=24
        self.assertEqual(GUI.opposite_door(self,0,10),(self.room_size-1,10))
        with self.assertRaises(ValueError):
            GUI.opposite_door(self, 2, 10)

    def test_get_adjacent_room(self):

        self.room_size=24
        room=Room(self.room_size, (1, 1))
        self.assertEqual(RoomArray.get_adjacent_room(self,room, (-1, 0)), (0, 1))
        self.assertNotEqual(RoomArray.get_adjacent_room(self,room, (1, 0)), (0, 1))


    def testing_player(self):

        self.player = Player()
        self.player.set_has_map()
        self.player.set_flippers()
        self.player.set_has_sling()
        self.player.set_heat_suit()

        self.assertTrue(self.player.get_has_map())
        self.assertTrue(self.player.get_has_sling())
        self.assertTrue(self.player.get_has_flippers())
        self.assertTrue(self.player.get_has_heat_suit())

    def testing_outer_walls(self):
        self.outer_wall_coords_4_by_4 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        self.outer_walls = []
        self.room_size = 4
        self.assertEqual(Tile.outer_walls_for_room_switches(self), self.outer_wall_coords_4_by_4)
        self.room_size = 5
        self.assertNotEqual(Tile.outer_walls_for_room_switches(self), self.outer_wall_coords_4_by_4)




if __name__ == '__main__':
    unittest.main()

