from PyQt5 import QtWidgets, QtCore, QtGui
import time

start_time = time.time()

from character_graphics_item import CharacterGraphicsItem
from chest_graphics import ChestGraphics
from monster_graphics import MonsterGraphics
from attack_graphics import AttackGraphics
from wall_graphics import WallGraphics
from floor_graphics import FloorGraphics
from lava_graphics import LavaGraphics
from fence_graphics import FenceGraphics
from target_graphics import TargetGraphics
from container import Container
from sign import Sign
from key import Key
from coin import Coin
from target import Target
from sling import Sling
from door_graphics import DoorGraphics
from switch_graphics import SwitchGraphics
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
from flippers import Flippers
from heat_suit import HeatSuit
from audio import Audio
from PyQt5.QtGui import QPainter, QPen
from random import randrange
from room import Room
from switch import Switch
from map import Map
from win_switch import WinSwitch
import math
from enemy import Enemy

"""
Notes for 2.0
need to make locations easier to get/standadise

charachters[0]=room.get....?This is rubbish.
split character graphics into individual methods, add monster add attack??
2nd..3rd..4th.. room
rooms with different dimensions rather than just square.
player animation
player damage
health meter
For Boss 4 enimies moving as one?
multi level map
needs scalability
TESTING!!
Lagless Sound!!!

Bugs

monster can die in front of the door blocking the way/ maybe make monster dissapear?/replaced with chest?
attack delay caused by sound
map to inventory switch


"""


class GUI(QtWidgets.QMainWindow):

    def __init__(self, room_1, tile_size, player, enemy):
        super().__init__()
        self.added_characters = []
        self.text_flag = 0
        self.flag_2 = 0
        self.walls_flag = 0
        self.is_paused = False
        self.player_x = None  # map X
        self.room_size = 24

        self.outer_walls = []
        self.outer_walls_for_room_switches()

        self.room_arr = [[None] * 4 for i in range(4)]
        self.room = room_1
        self.room2()
        self.room3()
        self.room4()
        self.room5()
        self.room6()
        self.room7()
        self.room8()
        self.room9()
        self.room10()
        self.room11()
        self.room12()
        self.room13()
        self.room14()
        self.room15()
        self.room16()

        self.say_hey()
        self.add_rooms_to_room_arr(self.room)

        self.current_room_num = 1
        self.room_map_index = 0

        self.player = player
        self.enemy_1 = enemy
        self.enemy_2 = Enemy(10)
        self.enemies = [self.enemy_1, self.enemy_2, None, None]  ##enemies for keypress event
        self.p_loc = None
        self.new_loc = None
        self.wall_random = []
        self.random_number_list_for_walls()
        self.finish_line = []
        self.finish_line_coords()

        self.signs = []
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)

        self.tile_size = tile_size
        self.init_window()
        self.add_room_graphics()
        self.add_instructions()
        self.walls = []  # list of wall graphic items so not randomised again when add room items called twice
        self.map = []

        self.inventory = None
        self.inventory_text_list = []
        # self.sound_effect = Audio()
        self.monster_to_remove = [None, None, None, None]
        self.player_to_remove = None
        self.attack_to_remove = None
        self.text_to_remove = None  ##Combine removes into 1 attribute?
        self.sign_to_remove = None
        self.enemy_drop = None
        self.water_to_remove = []
        self.lava_to_remove = []
        self.enemy_drop_flag = 0
        self.enemy_death_pos = [1, 1]  # this is a bug fix None None makes it crash if you enter room 0 1
        self.monster_graphic = [None, None, None, None]

        self.stone = None
        self.i_x = 0
        self.i_y = 0
        self.sling_flag = True

        self.sli_player_pos = None
        self.sli_player_facing = None

        self.enemy_drop_1_flag = False

        # self.add_character_graphics_items()
        # self.attack_graphic = AttackGraphics() #reduce latency?
        self.auto_move()
        # self.add_text()
        self.text = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.auto_move)
        self.timer.start(600)

        self.timer_2 = QtCore.QTimer()
        self.timer_2.timeout.connect(self.refresh)
        self.timer_2.start(10)

        self.timer_3 = QtCore.QTimer()  # attack timer
        self.timer_3.timeout.connect(self.attacking_to_false)
        self.timer_3.start(300)
        self.flag = 0  # sign

        self.timer_4 = QtCore.QTimer()
        self.timer_4.timeout.connect(self.sling)

        self.timer_5 = QtCore.QTimer()  # text hint timer, could have one timer
        self.timer_5.timeout.connect(self.close_text)

        self.timer_6 = QtCore.QTimer()
        self.timer_6.timeout.connect(self.add_water_animation)
        self.timer_6.start(1000)

        self.timer_7 = QtCore.QTimer()
        self.timer_7.timeout.connect(self.add_lava_animation)
        self.timer_7.start(600)

        self.effect = QSoundEffect()
        self.sound_file = 'audio/zap_2.wav'
        self.effect.setSource(QUrl.fromLocalFile(self.sound_file))
        # effect.setLoopCount(QSoundEffect.Infinite)
        self.effect.setVolume(0.25);

        self.map_graphic_items = []
        self.end_game_flag = False

    def keyPressEvent(self, event):

        characters = self.room.get_characters_in_room()
        player = characters[0]
        switches = self.room.get_switches_in_room()
        player_loc = player.get_location()

        switch_count = 0
        num_of_switch_ons = 0

        for switch in switches:
            if player_loc == switch.get_location():
                switch.switch__on_off()
                self.add_room_graphics()
            switch_count += 1

        if self.end_game_flag and event.key() == QtCore.Qt.Key_Q:
            quit()

        if event.key() == QtCore.Qt.Key_W and not self.is_paused:

            if player.get_facing() == (0, -1):

                player.set_location(player_loc[0], player_loc[1] - 1, self.room)

                if player.get_location() in self.outer_walls and event.key() == QtCore.Qt.Key_W:
                    additonal_tile = player.get_facing()

                    for x in self.room.tiles:  # clearing enimies for next room load
                        for y in x:

                            if y.get_character() is not None:
                                if y.get_character().get_character_type() == 'enemy':
                                    y.clear_character()

                    self.add_rooms_to_room_arr(self.room)
                    self.p_loc = player.get_location()

                    self.room = self.get_room_by_coords(self.get_adjacent_room(self.room, player.get_facing()))

                    self.new_loc = self.opposite_door(self.p_loc[0], self.p_loc[1])

                    self.room.tiles[self.new_loc[0]][self.new_loc[1]].clear_character()
                    self.room.tiles[self.new_loc[0] + additonal_tile[0]][
                        self.new_loc[1] + additonal_tile[1]].clear_character()

                    player.set_location(self.new_loc[0], self.new_loc[1] - 1, self.room)
                    if self.room.get_coordinates() != (3, 1):
                        self.enemies[0].set_location(1, 10, self.room)
                        self.enemies[0].set_is_alive(True)
                        self.enemies[1].set_location(20, 11, self.room)
                        self.enemies[1].set_is_alive(True)

                    self.add_room_graphics()
                    self.add_character_graphics_items()
                    self.add_room_graphics()
                    self.refresh()

            else:

                player.set_facing((0, -1))


        elif event.key() == QtCore.Qt.Key_S and not self.is_paused:

            if player.get_facing() == (0, 1):

                player.set_location(player_loc[0], player_loc[1] + 1, self.room)

                if player.get_location() in self.outer_walls and event.key() == QtCore.Qt.Key_S:
                    additonal_tile = player.get_facing()

                    self.room.tiles[self.enemy_death_pos[0]][self.enemy_death_pos[1]].clear_character()
                    for x in self.room.tiles:  # clearing enimies for next room load
                        for y in x:

                            if y.get_character() is not None:
                                if y.get_character().get_character_type() == 'enemy':
                                    y.clear_character()

                    self.add_rooms_to_room_arr(self.room)
                    self.p_loc = player.get_location()
                    self.room = self.get_room_by_coords(self.get_adjacent_room(self.room, player.get_facing()))

                    self.new_loc = self.opposite_door(self.p_loc[0], self.p_loc[1])

                    self.room.tiles[self.new_loc[0]][self.new_loc[1]].clear_character()
                    self.room.tiles[self.new_loc[0] + additonal_tile[0]][
                        self.new_loc[1] + additonal_tile[1]].clear_character()
                    player.set_location(self.new_loc[0], self.new_loc[1] + 1, self.room)

                    if self.room.get_coordinates() != (3, 3):
                        self.enemies[0].set_location(2, 2,
                                                     self.room)  # enimies need to be set in rooms or seperate method?
                        self.enemies[0].set_is_alive(True)

                    self.add_room_graphics()
                    self.add_character_graphics_items()
                    self.refresh()

                if self.room.get_coordinates() == (3, 3):

                    if player.get_location() in self.finish_line:
                        self.is_paused = True
                        self.win_game_message()

            else:

                player.set_facing((0, 1))



        elif event.key() == QtCore.Qt.Key_A and not self.is_paused:
            if player.get_facing() == (-1, 0):

                player.set_location(player_loc[0] - 1, player_loc[1], self.room)

                if player.get_location() in self.outer_walls and event.key() == QtCore.Qt.Key_A:
                    additonal_tile = player.get_facing()

                    for x in self.room.tiles:  # clearing enimies for next room load
                        for y in x:

                            if y.get_character() is not None:
                                if y.get_character().get_character_type() == 'enemy':
                                    y.clear_character()

                    self.add_rooms_to_room_arr(self.room)
                    self.p_loc = player.get_location()
                    self.room = self.get_room_by_coords(self.get_adjacent_room(self.room, player.get_facing()))
                    self.current_room_num = 1
                    self.new_loc = self.opposite_door(self.p_loc[0], self.p_loc[1])

                    self.room.tiles[self.new_loc[0]][self.new_loc[1]].clear_character()
                    self.room.tiles[self.new_loc[0] + additonal_tile[0]][
                        self.new_loc[1] + additonal_tile[1]].clear_character()
                    player.set_location(self.new_loc[0] - 1, self.new_loc[1], self.room)

                    self.add_room_graphics()
                    self.add_character_graphics_items()
                    self.refresh()


            else:

                player.set_facing((-1, 0))


        elif event.key() == QtCore.Qt.Key_D and not self.is_paused:  # attack

            if player.get_facing() == (1, 0):

                player.set_location(player_loc[0] + 1, player_loc[1], self.room)

                if player.get_location() in self.outer_walls and event.key() == QtCore.Qt.Key_D:
                    additonal_tile = player.get_facing()

                    for x in self.room.tiles:  # clearing enimies for next room load
                        for y in x:

                            if y.get_character() is not None:
                                if y.get_character().get_character_type() == 'enemy':
                                    y.clear_character()

                    self.add_rooms_to_room_arr(self.room)
                    self.p_loc = player.get_location()
                    self.room = self.get_room_by_coords(self.get_adjacent_room(self.room, player.get_facing()))
                    self.current_room_num = 1

                    self.new_loc = self.opposite_door(self.p_loc[0], self.p_loc[1])

                    self.room.tiles[self.new_loc[0]][self.new_loc[1]].clear_character()
                    self.room.tiles[self.new_loc[0] + additonal_tile[0]][
                        self.new_loc[1] + additonal_tile[1]].clear_character()
                    player.set_location(self.new_loc[0] + 1, self.new_loc[1], self.room)
                    if self.room.get_coordinates() != (3, 1) and self.room.get_coordinates() != (1, 1):
                        self.enemies[0].set_location(10, 10, self.room)
                        self.enemies[0].set_is_alive(True)
                        self.enemies[1].set_location(11, 11, self.room)
                        self.enemies[1].set_is_alive(True)
                    self.add_room_graphics()
                    self.add_character_graphics_items()
                    self.refresh()

            else:

                player.set_facing((1, 0))

        elif event.key() == QtCore.Qt.Key_P and not self.is_paused:

            player.set_attacking(True)

            self.play_sound()





        elif event.key() == QtCore.Qt.Key_Y and not self.is_paused:  # sling
            characters = self.room.get_characters_in_room()
            player = characters[0]
            if player.get_has_sling():
                self.sli_player_pos = player.get_location()

                self.sli_player_facing = player.get_facing()

                self.sling()


        elif event.key() == QtCore.Qt.Key_M and player.get_has_map():  # Pause /map KEY

            if not self.is_paused:
                self.timer.stop()
                self.timer_2.stop()
                self.timer_3.stop()
                self.is_paused = True
                self.map_window()

            else:

                self.timer.start(200)
                self.timer_2.start(10)
                self.timer_3.start(100)
                self.is_paused = False
                self.map_window()


        elif event.key() == QtCore.Qt.Key_I:

            if self.is_paused == False:
                self.timer.stop()
                self.timer_2.stop()
                self.timer_3.stop()
                self.is_paused = True
                self.inventory_window()

            elif self.is_paused == True:
                self.timer.start(200)
                self.timer_2.start(10)
                self.timer_3.start(100)
                self.is_paused = False
                self.inventory_window()

        self.room.tiles[player_loc[0]][
            player_loc[1]].clear_character()  ##remove character from tile so player can go back

        for x in self.room.tiles:
            for y in x:

                if y.is_door_tile() and player.get_has_key() \
                        and self.calculate_distance(y.get_location(),
                                                    player_loc) == 1.0 and event.key() == QtCore.Qt.Key_O and not self.is_paused:

                    if self.room.get_coordinates() != (0, 2):
                        y.set_door(False)
                        player.set_key(False)
                        player.remove_from_inventory('key')
                        self.add_text("Key removed.")
                        self.add_room_graphics()
                    else:
                        self.add_text("That key does not work here.")
                        self.add_room_graphics()


                elif y.is_door_tile() and self.room.all_switches_are_on():
                    y.set_door(False)
                    self.add_room_graphics()

                elif y.is_door_tile() and self.room.all_targets_are_hit():
                    y.set_door(False)
                    self.add_room_graphics()

        for x in self.room.tiles:
            for y in x:

                if y.is_container_tile():
                    container = y.get_container()
                    container_pos = container.get_location()

                    if event.key() == QtCore.Qt.Key_O and not self.is_paused:

                        if self.calculate_distance(container_pos, player_loc) == 1 and container.get_item() != None:
                            if container.get_item().get_type() != 'coin':
                                player.add_to_inventory(container.get_item())
                            if container.get_item().get_type() == 'key':

                                player.set_key(True)
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_text("You have a Key.")
                                self.add_room_graphics()


                            elif container.get_item().get_type() == 'flippers':
                                self.add_text("You have the flippers.")
                                player.set_flippers()
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_room_graphics()

                            elif container.get_item().get_type() == 'heat suit':
                                self.add_text("You have the the heat suit.")
                                player.set_heat_suit()
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_room_graphics()

                            elif container.get_item().get_type() == 'coin':

                                value = container.get_item().get_value()

                                self.add_text("You have found {} coins.".format(value))
                                player.add_to_wallet(value)
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_room_graphics()

                            elif container.get_item().get_type() == 'sling':

                                self.add_text("You have found the sling shot.")
                                player.set_has_sling()
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_instructions()
                                self.add_room_graphics()

                            elif container.get_item().get_type() == 'map':

                                self.add_text("You have found the Map.")
                                player.set_has_map()
                                container.set_item(None)
                                container.set_is_full(False)
                                self.add_instructions()
                                self.add_room_graphics()

        for x in self.room.tiles:
            for y in x:
                if y.is_sign_tile():
                    if self.calculate_distance(player_loc,
                                               y.get_sign().get_location()) == 1 and not self.is_paused and event.key() == QtCore.Qt.Key_O:
                        self.sign_read(y.get_sign())

    def refresh(self):

        self.update_characters()
        self.add_character_graphics_items()

    def attacking_to_false(self):

        characters = self.room.get_characters_in_room()
        characters[0].set_attacking(False)
        # self.timer_3.stop()

    def auto_move(self):

        characters = self.room.get_characters_in_room()
        i = 1
        if not self.is_paused:
            while i < len(characters):
                rn2 = randrange(4)
                enemy = characters[i]

                enemy_pos = enemy.get_location()

                if rn2 == 0 and enemy.get_is_alive():

                    enemy.set_facing((0, 1))
                    enemy.set_location(enemy_pos[0], enemy_pos[1] + 1, self.room)
                    self.room.tiles[enemy_pos[0]][enemy_pos[1]].clear_character()


                elif rn2 == 1 and enemy.get_is_alive():

                    enemy.set_facing((0, -1))
                    enemy.set_location(enemy_pos[0], enemy_pos[1] - 1, self.room)
                    self.room.tiles[enemy_pos[0]][enemy_pos[1]].clear_character()


                elif rn2 == 2 and enemy.get_is_alive():

                    enemy.set_facing((1, 0))
                    enemy.set_location(enemy_pos[0] + 1, enemy_pos[1], self.room)
                    self.room.tiles[enemy_pos[0]][enemy_pos[1]].clear_character()


                elif rn2 == 3 and enemy.get_is_alive():

                    enemy.set_facing((-1, 0))
                    enemy.set_location(enemy_pos[0] - 1, enemy_pos[1], self.room)
                    self.room.tiles[enemy_pos[0]][enemy_pos[1]].clear_character()
                i += 1

    def init_window(self):

        self.setGeometry(330, 330, 800, 800)
        self.setWindowTitle('Adventure')
        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 800)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()

    def map_window(self):

        map_t_size = 6

        room_size = self.room_size * map_t_size

        map_rect = QtCore.QRectF(100, 100, room_size * 4, room_size * 4)
        map_item = QtWidgets.QGraphicsRectItem(map_rect)
        map_item.setBrush(QtGui.QColor(200, 200, 200))
        self.scene.addItem(map_item)
        self.map.append(map_item)

        if self.is_paused:
            for rooms in self.room_arr:
                for room in rooms:
                    if room != None:
                        characters = room.get_characters_in_room()
                        r_coords = room.get_coordinates()
                        for x in room.tiles:
                            for y in x:
                                if y.is_wall_tile():
                                    p = y.get_location()
                                    map_wall_rect = QtCore.QRectF(p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                                                  p[1] * map_t_size + (r_coords[1] * room_size) + 100,
                                                                  map_t_size, map_t_size)
                                    map_wall_item = QtWidgets.QGraphicsRectItem(map_wall_rect)
                                    map_wall_item.setBrush(QtGui.QColor(255, 165, 0))
                                    self.map_graphic_items.append(map_wall_item)
                                    self.scene.addItem(map_wall_item)

                                elif y.get_is_water():

                                    p = y.get_location()
                                    map_water_rect = QtCore.QRectF(p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                                                   p[1] * map_t_size + (r_coords[1] * room_size) + 100,
                                                                   map_t_size, map_t_size)
                                    map_water_item = QtWidgets.QGraphicsRectItem(map_water_rect)
                                    map_water_item.setBrush(QtGui.QColor(0, 71, 100))
                                    self.map_graphic_items.append(map_water_item)
                                    self.scene.addItem(map_water_item)

                                elif y.is_door_tile():

                                    p = y.get_location()
                                    map_door_rect = QtCore.QRectF(p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                                                  p[1] * map_t_size + (r_coords[1] * room_size) + 100,
                                                                  map_t_size, map_t_size)
                                    map_door_item = QtWidgets.QGraphicsRectItem(map_door_rect)
                                    map_door_item.setBrush(QtGui.QColor(150, 75, 0))
                                    self.map_graphic_items.append(map_door_item)
                                    self.scene.addItem(map_door_item)

                                elif y.is_container_tile():

                                    p = y.get_location()
                                    if y.get_container().get_is_full():
                                        map_container_rect = QtCore.QRectF(
                                            p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                            p[1] * map_t_size + (r_coords[1] * room_size) + 100, map_t_size, map_t_size)
                                        map_container_item = QtWidgets.QGraphicsRectItem(map_container_rect)
                                        map_container_item.setBrush(QtGui.QColor(255, 215, 0))
                                        self.map_graphic_items.append(map_container_item)
                                        self.scene.addItem(map_container_item)
                                    else:
                                        map_container_rect = QtCore.QRectF(
                                            p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                            p[1] * map_t_size + (r_coords[1] * room_size) + 100, map_t_size, map_t_size)
                                        map_container_item = QtWidgets.QGraphicsRectItem(map_container_rect)

                                        self.map_graphic_items.append(map_container_item)
                                        self.scene.addItem(map_container_item)



                                elif y.get_is_lava():

                                    p = y.get_location()
                                    map_lava_rect = QtCore.QRectF(p[0] * map_t_size + (r_coords[0] * room_size) + 100,
                                                                  p[1] * map_t_size + (r_coords[1] * room_size) + 100,
                                                                  map_t_size, map_t_size)
                                    map_lava_item = QtWidgets.QGraphicsRectItem(map_lava_rect)
                                    map_lava_item.setBrush(QtGui.QColor(205, 0, 0))
                                    self.map_graphic_items.append(map_lava_item)
                                    self.scene.addItem(map_lava_item)

                                if len(characters) > 0:
                                    if room.get_coordinates() == characters[0].get_current_room():
                                        self.scene.removeItem(self.player_x)
                                        self.player_x = QtWidgets.QGraphicsTextItem()
                                        self.player_x.setDefaultTextColor(QtGui.QColor(255, 0, 0))
                                        self.player_x.setPlainText('X')

                                        player_pos = characters[0].get_location()
                                        self.player_x.setPos(
                                            map_t_size * player_pos[0] + (r_coords[0] * room_size) + 95,
                                            map_t_size * player_pos[1] + (r_coords[1] * room_size) + 95)

                                        self.scene.addItem(self.player_x)



        elif self.is_paused == False:
            i = 0

            while i < len(self.map_graphic_items):
                self.scene.removeItem(self.map_graphic_items[i])
                i += 1

            self.scene.removeItem(self.player_x)

            i = 0
            while i < len(self.map):
                self.scene.removeItem(self.map[i])
                i += 1

            self.map_graphic_items = []

    def create_container(self):

        characters = self.room.get_characters_in_room()
        enemy_pos = characters[1].get_location()
        self.enemy_drop = Container()

        key_2 = Key("key")

        if self.enemy_drop_1_flag == False:
            self.enemy_drop.set_location(20, 20, self.room)
            self.enemy_drop.set_item(key_2)
            self.enemy_drop_1_flag = True

        self.add_room_graphics()

    def inventory_window(self):

        characters = self.room.get_characters_in_room()
        player = characters[0]
        inventory = player.get_inventory()
        if self.is_paused:
            self.inventory = QtCore.QRectF(200, 100, 200, 200)
            self.inventory = QtWidgets.QGraphicsRectItem(self.inventory)
            self.inventory.setBrush(QtGui.QColor(200, 200, 200))
            self.scene.addItem(self.inventory)
            across = 200
            down = 110
            for x in inventory:
                self.inventory_text = QtWidgets.QGraphicsTextItem()
                self.inventory_text.setPlainText(x.get_name())
                self.inventory_text.setPos(across, down)
                self.inventory_text_list.append(self.inventory_text)
                self.scene.addItem(self.inventory_text)
                down += 15
            down += 15
            self.inventory_text = QtWidgets.QGraphicsTextItem()
            self.inventory_text.setPlainText("You have {} gold coins".format(player.get_wallet()))
            self.inventory_text.setPos(across, down)
            self.wallet_to_remove = self.inventory_text
            self.scene.addItem(self.inventory_text)

        if self.is_paused == False:
            i = 0
            for x in inventory:
                self.scene.removeItem(self.inventory_text_list[i])
                i += 1

            self.inventory_text_list = []
            self.scene.removeItem(self.inventory)
            self.scene.removeItem(self.wallet_to_remove)

    def sling(self):

        self.timer_4.start(50)
        self.sling_shot()

    def sling_shot(self):

        characters = self.room.get_characters_in_room()
        if len(characters) > 1:
            enemy = characters[1]
        i = 1
        self.scene.removeItem(self.stone)

        self.room.tiles[self.sli_player_pos[0] + self.sli_player_facing[0] + self.i_x][
            self.sli_player_pos[1] + self.sli_player_facing[1] + self.i_y].set_is_stone()
        self.sling_flag = self.room.tiles[self.sli_player_pos[0] + self.sli_player_facing[0] + self.i_x][
            self.sli_player_pos[1] + self.sli_player_facing[1] + self.i_y].get_is_stone()
        self.stone = QtWidgets.QGraphicsTextItem()
        self.stone.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        self.stone.setPlainText(' o')

        self.stone.setPos((self.sli_player_pos[0] + self.sli_player_facing[0] + self.i_x) * self.tile_size,
                          (self.sli_player_pos[1] + self.sli_player_facing[1] + self.i_y) * self.tile_size)
        self.scene.addItem(self.stone)
        self.i_x += self.sli_player_facing[0]
        self.i_y += self.sli_player_facing[1]

        if self.sling_flag == False:

            t_flag = False

            for x in self.room.tiles:
                for y in x:
                    if y.is_target_tile():
                        t_location = y.get_location()
                        t_flag = True
                        target = y.get_target()

            if t_flag == True:
                for x in self.room.tiles:
                    for y in x:

                        if len(characters) > 1:
                            if y.get_is_stone() == True and y.get_location() == enemy.get_location():
                                enemy.set_is_alive(False)
                                self.enemy_death_pos = characters[1].get_location()
                                self.add_room_graphics()
                                y.set_is_stone()

                        if y.get_is_stone():

                            y.set_is_stone()
                            print(y.get_location())

                            if self.calculate_distance(y.get_location(), t_location) == 1:
                                print(3)
                                target.switch__on_off()
                                self.add_room_graphics()

                        if y.is_target_tile() and y.set_is_stone():
                            pass

            else:
                for x in self.room.tiles:
                    for y in x:

                        if len(characters) > 1:
                            if y.get_is_stone() == True and y.get_location() == enemy.get_location():
                                enemy.set_is_alive(False)
                                self.enemy_death_pos = characters[1].get_location()
                                self.add_room_graphics()
                                y.set_is_stone()

                        if y.get_is_stone():
                            y.set_is_stone()

                        if y.is_target_tile() and y.set_is_stone():
                            pass

            """
            if self.calculate_distance(((self.sli_player_pos[0] + self.sli_player_facing[0] + self.i_x)(self.sli_player_pos[1] + self.sli_player_facing[1] + self.i_y)),t_location) == 1:

                self.add_room_graphics()
            """

            i += 1
            self.i_x = 0
            self.i_y = 0

            self.scene.removeItem(self.stone)
            self.timer_4.stop()

    def sling_damage(self, target):

        target.set_is_alive(False)
        self.enemy_death_pos = target.get_location()
        self.create_container()
        self.add_room_graphics()

    def add_room_graphics(self):  # have room passed to here for creating multiple rooms?

        across = 0
        down = 0
        i = 0
        for x in self.room.tiles:
            for y in x:
                if y.is_wall_tile() and self.walls_flag == 0:
                    p_wall = y.get_location()
                    wall = WallGraphics(self.wall_random[i])
                    wall.setPos(p_wall[0] * self.tile_size, p_wall[1] * self.tile_size)
                    self.scene.addItem(wall)
                    across += self.tile_size
                    i += 1

                elif y.is_container_tile():

                    c = y.get_container()
                    p = y.get_location()

                    if c.get_is_full():
                        f_chest = ChestGraphics(1)
                        f_chest.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(f_chest)

                    else:
                        e_chest = ChestGraphics(0)
                        e_chest.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(e_chest)

                    across += self.tile_size

                elif y.get_is_water():

                    p_water = y.get_location()
                    water = FloorGraphics(randrange(6))
                    water.setPos(p_water[0] * self.tile_size, p_water[1] * self.tile_size)
                    self.scene.addItem(water)
                    across += self.tile_size

                elif y.get_is_lava():

                    p_lava = y.get_location()
                    lava = LavaGraphics(randrange(6))
                    lava.setPos(p_lava[0] * self.tile_size, p_lava[1] * self.tile_size)
                    self.scene.addItem(lava)
                    across += self.tile_size

                elif y.get_is_fence():

                    p_fence = y.get_location()
                    fence = FenceGraphics(0)
                    fence.setPos(p_fence[0] * self.tile_size, p_fence[1] * self.tile_size)
                    self.scene.addItem(fence)

                    across += self.tile_size


                elif y.is_door_tile():
                    p_door = y.get_location()
                    door = DoorGraphics()
                    door.setPos(p_door[0] * self.tile_size, p_door[1] * self.tile_size)
                    self.scene.addItem(door)
                    across += self.tile_size

                elif y.is_sign_tile():

                    self.scene.addRect(down, across, self.tile_size, self.tile_size).setBrush(
                        QtGui.QColor(200, 200, 200))
                    sign_graphic = ChestGraphics(2)
                    sign_pos = y.get_location()
                    sign_graphic.setPos(sign_pos[0] * self.tile_size, sign_pos[1] * self.tile_size)
                    self.signs.append(y.get_sign())

                    self.scene.addItem(sign_graphic)
                    across += self.tile_size

                elif y.is_switch_tile():

                    c = y.get_switch()
                    p = y.get_location()

                    if c.get_is_on():
                        on_switch = SwitchGraphics(0)
                        on_switch.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(on_switch)

                    else:
                        off_switch = SwitchGraphics(1)
                        off_switch.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(off_switch)

                    across += self.tile_size

                elif y.is_target_tile():

                    c = y.get_target()
                    p = y.get_location()

                    if c.get_is_on():

                        on_target = TargetGraphics(1)
                        on_target.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(on_target)


                    else:

                        off_target = TargetGraphics(0)
                        off_target.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(off_target)

                    across += self.tile_size

                elif y.is_win_switch_tile():

                    c = y.get_win_switch()
                    p = y.get_location()

                    if c.get_is_on():
                        off_switch = SwitchGraphics(2)
                        off_switch.setPos(p[0] * self.tile_size, p[1] * self.tile_size)
                        self.scene.addItem(off_switch)

                    across += self.tile_size

                else:
                    col_alt = self.wall_random[i] * self.wall_random[i]
                    self.scene.addRect(down, across, self.tile_size, self.tile_size).setBrush(
                        QtGui.QColor(200 + col_alt, 200 + (col_alt * 2), 200 + col_alt))
                    across += self.tile_size

            across = 0
            down += self.tile_size

    def add_water_animation(self):

        if not self.is_paused:
            across = 0
            down = 0
            i = 0
            while i < len(self.water_to_remove):
                self.scene.removeItem(self.water_to_remove[i])
                i += 1
            self.water_to_remove = []

            for x in self.room.tiles:

                for y in x:

                    if y.get_is_water():
                        p_water = y.get_location()
                        water = FloorGraphics(randrange(6))
                        water.setPos(p_water[0] * self.tile_size, p_water[1] * self.tile_size)
                        self.scene.addItem(water)
                        self.water_to_remove.append(water)
                        across += self.tile_size

    def add_lava_animation(self):

        if not self.is_paused:
            across = 0
            down = 0
            i = 0
            while i < len(self.lava_to_remove):
                self.scene.removeItem(self.lava_to_remove[i])
                i += 1
            self.lava_to_remove = []

            for x in self.room.tiles:

                for y in x:

                    if y.get_is_lava():
                        p_lava = y.get_location()
                        lava = LavaGraphics(randrange(6))
                        lava.setPos(p_lava[0] * self.tile_size, p_lava[1] * self.tile_size)
                        self.scene.addItem(lava)
                        self.lava_to_remove.append(lava)
                        across += self.tile_size

    def add_text(self, message):

        characters = self.room.get_characters_in_room()
        self.scene.removeItem(self.text)

        self.text = QtWidgets.QGraphicsTextItem()
        self.text.setPlainText(message)
        self.text.setPos(620, 60)

        self.scene.addItem(self.text)
        self.timer_5.start(4000)

    def close_text(self):

        print("what")
        self.scene.removeItem(self.text)  # This doesn't work see above **
        self.timer_5.stop()

    def win_game_message(self):

        self.end_game_flag = True
        characters = self.room.get_characters_in_room()
        player = characters[0]
        inventory = player.get_inventory()
        if self.is_paused:

            time_min, time_sec = divmod((time.time() - start_time), 60)

            self.inventory = QtCore.QRectF(100, 100, 400, 420)
            self.inventory = QtWidgets.QGraphicsRectItem(self.inventory)
            self.inventory.setBrush(QtGui.QColor(100, 100, 200))
            self.scene.addItem(self.inventory)

            self.inventory_text = QtWidgets.QGraphicsTextItem()
            self.inventory_text.setPlainText("CONGRATULATIONS YOU HAVE COMPLETED ")
            self.inventory_text.setPos(100, 110)
            self.inventory_text_list.append(self.inventory_text)
            self.scene.addItem(self.inventory_text)

            self.inventory_text = QtWidgets.QGraphicsTextItem()
            self.inventory_text.setPlainText("'Y2 THE ADVENTURE'")
            self.inventory_text.setPos(100, 125)
            self.inventory_text_list.append(self.inventory_text)
            self.scene.addItem(self.inventory_text)

            self.inventory_text = QtWidgets.QGraphicsTextItem()
            if time_min == 1:
                self.inventory_text.setPlainText(
                    "YOUR TIME WAS: {} minute and {:.2f} seconds. ".format(int(time_min), float(time_sec)))
            else:
                self.inventory_text.setPlainText(
                    "YOUR TIME WAS: {} minutes and {:.2f} seconds. ".format(int(time_min), float(time_sec)))
            self.inventory_text.setPos(100, 160)
            self.inventory_text_list.append(self.inventory_text)
            self.scene.addItem(self.inventory_text)

            self.inventory_text = QtWidgets.QGraphicsTextItem()
            self.inventory_text.setPlainText("YOU FOUND {} COINS. ".format(player.get_wallet()))
            self.inventory_text.setPos(100, 175)
            self.inventory_text_list.append(self.inventory_text)
            self.scene.addItem(self.inventory_text)

            self.inventory_text = QtWidgets.QGraphicsTextItem()
            self.inventory_text.setPlainText("Thanks for playing, press 'Q' to quit")
            self.inventory_text.setPos(100, 200)
            self.inventory_text_list.append(self.inventory_text)
            self.scene.addItem(self.inventory_text)

    def add_instructions(self):
        characters = self.room.get_characters_in_room()
        player = characters[0]

        if player.get_has_sling():
            self.scene.addText("Y is slingshot").setPos(500, 675)

        elif player.get_has_map() and not player.get_has_sling():
            self.scene.addText(
                "M for map").setPos(500, 660)

        else:
            self.scene.addText(
                "W S A D to Move \nO to open\nP to attack\nI for inventory\n").setPos(500, 600)

    def sign_read(self, sign):

        sign_text = QtWidgets.QGraphicsTextItem()
        sign_text.setPlainText(sign.get_message())
        pos = sign.get_location()
        sign_text.setPos((pos[0] - 3) * self.tile_size, (pos[1] - 1) * self.tile_size)

        if self.flag == 0:
            self.scene.addItem(sign_text)
            self.sign_to_remove = sign_text
            self.flag = 1


        elif self.flag == 1:

            self.scene.removeItem(self.sign_to_remove)

            self.flag = 0

    def update_characters(self):

        for character in self.added_characters:
            character.updateAll()

    def add_character_graphics_items(self):  # have room passed to here for creating multiple rooms?

        characters = self.room.get_characters_in_room()  #
        character_pos = []
        character_facing = []
        player_graphic = None
        attack_pos = []

        for x in characters:  # loops through all characters
            player_graphic = (
                CharacterGraphicsItem(characters[0], self.tile_size))  # add player polygon graphics item to list
            character_pos.append(x.get_location())  # get monster and player positions
            character_facing.append(x.get_facing())  # get facing positions

        self.scene.removeItem(self.player_to_remove)  ## removes the player graphic added on the previous method call.
        self.scene.addItem(player_graphic)  # add player graphics item to scene
        self.player_to_remove = player_graphic  # updating player graphic to remove for net call

        ##Adding weapon graphic item in correct square and with correct orrientation

        if self.flag_2 == 1:  # only implement after 1st attack
            self.scene.removeItem(self.attack_to_remove)

        if characters[0].get_attacking():
            attack_pos.append(character_pos[0][0])
            attack_pos.append(character_pos[0][1])
            attack = AttackGraphics(characters[0], self.tile_size)

            if attack.get_rot_angle() == 90:

                attack.setPos((attack_pos[0] + 2) * self.tile_size, (attack_pos[1]) * self.tile_size)

            elif attack.get_rot_angle() == 180:

                attack.setPos((attack_pos[0] + 1) * self.tile_size, (attack_pos[1] + 2) * self.tile_size)

            elif attack.get_rot_angle() == 270:

                attack.setPos((attack_pos[0] - 1) * self.tile_size, (attack_pos[1] + 1) * self.tile_size)

            elif attack.get_rot_angle() == 0:

                attack.setPos(attack_pos[0] * self.tile_size, (attack_pos[1] - 1) * self.tile_size)

            self.attack_to_remove = attack  # similar implementation to the remove/add/update_remove system used for player
            self.scene.addItem(attack)
            self.flag_2 = 1

        if len(characters) > 1:
            i = 1
            while i < len(characters):
                if characters[0].get_attacking() and self.calculate_distance(attack_pos, character_pos[
                    i]) == 1:  # Finds the distance between the attack and enemy

                    characters[i].set_is_alive(False)  # Kills enemy if attack is close enough
                    self.enemy_death_pos = characters[
                        i].get_location()  # records the death position, this is needed when moving between rooms to remove previous enemy

                    self.create_container()  # creates container for enmey item drop

                self.scene.removeItem(self.monster_to_remove[i - 1])
                self.monster_graphic[i - 1] = MonsterGraphics()  # create monster graphic

                self.monster_graphic[i - 1].setPos(character_pos[i][0] * self.tile_size,
                                                   character_pos[i][1] * self.tile_size)  # position monster graphic
                self.monster_to_remove[i - 1] = self.monster_graphic[i - 1]
                self.scene.addItem(self.monster_graphic[i - 1])  # add monster graphic
                i += 1

    def random_number_list_for_walls(self):
        # this is seperate as random numbers are wanted for first wall creation but the same walls when added to scene again
        for x in self.room.tiles:
            for y in x:
                self.wall_random.append(randrange(4))

    def play_sound(self):

        self.effect.play()

    def calculate_distance(self, cord_1, cord_2):
        # Used to calculate the distance between two room coordinates
        ret = math.sqrt((cord_2[0] - cord_1[0]) ** 2 + (cord_1[1] - cord_2[1]) ** 2)

        return ret

    """
    Here we create additional rooms, The external wall is created by the call to Room()
    the internal walls are then created within the method. Doors can then be added. Doors are added then removed
    to create gaps in walls,    

    """

    def room2(self):

        room_2 = Room(self.room_size, (1, 0))

        for i in range(1, 10):
            room_2.tiles[i][13].set_wall()
            room_2.tiles[i][9].set_wall()

        for i in range(15, self.room_size):
            room_2.tiles[i][13].set_wall()
            room_2.tiles[i][9].set_wall()

        room_2.tiles[12][self.room_size - 1].set_door(True)  # exterior door
        room_2.tiles[12][self.room_size - 1].set_door(False)
        room_2.tiles[0][8].set_door(True)  # exterior door
        room_2.tiles[0][8].set_door(False)
        room_2.tiles[self.room_size - 1][5].set_door(True)
        room_2.tiles[self.room_size - 1][5].set_door(False)

        for i in range(11, 13):
            room_2.tiles[9][i].set_wall()
            room_2.tiles[15][i].set_wall()

        chest_2 = Container()
        coin_2 = Coin("coin", 2)
        chest_2.set_location(11, 1, room_2)
        chest_2.set_item(coin_2)

        chest_3 = Container()
        coin_3 = Coin("coin", 4)
        chest_3.set_location(12, 1, room_2)
        chest_3.set_item(coin_3)

        chest_4 = Container()
        coin_4 = Coin("coin", 3)
        chest_4.set_location(13, 1, room_2)
        chest_4.set_item(coin_4)

        room_2.tiles[10][1].set_wall()
        room_2.tiles[14][1].set_wall()
        self.add_rooms_to_room_arr(room_2)

    def room3(self):

        room_3 = Room(self.room_size, (0, 0))

        chest = Container()
        chest.set_location(17, 17, room_3)
        flippers_1 = Flippers("flippers")
        chest.set_item(flippers_1)

        switch = Switch()
        switch.set_location(3, 3, room_3)
        switch_2 = Switch()
        switch_2.set_location(3, 7, room_3)
        switch_3 = Switch()
        switch_3.set_location(7, 3, room_3)
        switch_4 = Switch()
        switch_4.set_location(7, 7, room_3)
        for i in range(11):
            room_3.tiles[i][10].set_wall()
            room_3.tiles[10][i].set_wall()

        room_3.tiles[5][10].set_door(True)
        room_3.tiles[5][10].set_door(False)

        room_3.tiles[12][15].set_door(True)
        for i in range(self.room_size):
            room_3.tiles[i][15].set_wall()

        room_3.tiles[self.room_size - 1][8].set_door(True)
        room_3.tiles[self.room_size - 1][8].set_door(False)

        self.add_rooms_to_room_arr(room_3)

    def room4(self):

        room_4 = Room(self.room_size, (0, 1))

        for i in range(11, self.room_size):
            for k in range(self.room_size - 1):
                room_4.tiles[k][i].set_water()
                room_4.tiles[k][i].set_water()
                room_4.tiles[k][i].set_water()

        sign = Sign("The water is too deep to swim unaided")
        room_4.tiles[5][5].set_sign(sign)

        chest = Container()
        map = Map('map')
        chest.set_location(4, 2, room_4)
        chest.set_item(map)

        room_4.tiles[self.room_size - 1][8].set_door(True)
        room_4.tiles[self.room_size - 1][8].set_door(False)
        room_4.tiles[5][self.room_size - 1].set_door(True)
        room_4.tiles[5][self.room_size - 1].set_door(False)
        self.add_rooms_to_room_arr(room_4)

    def room5(self):

        room_5 = Room(self.room_size, (1, 2))
        chest = Container()
        chest.set_location(8, 8, room_5)
        heat_suit_1 = HeatSuit("heat suit")
        chest.set_item(heat_suit_1)
        room_5.tiles[12][15].set_door(True)
        for i in range(self.room_size):
            room_5.tiles[i][15].set_wall()
        for i in range(15, self.room_size):
            room_5.tiles[13][i].set_wall()

        room_5.tiles[0][self.room_size - 3].set_door(True)
        room_5.tiles[0][self.room_size - 3].set_door(False)
        room_5.tiles[self.room_size - 1][20].set_door(True)
        room_5.tiles[self.room_size - 1][20].set_door(False)
        room_5.tiles[19][self.room_size - 1].set_door(True)

        self.add_rooms_to_room_arr(room_5)

    def room6(self):
        room_6 = Room(self.room_size, (0, 2))
        for i in range(self.room_size):
            room_6.tiles[8][i].set_wall()
            room_6.tiles[12][i].set_wall()
            room_6.tiles[16][i].set_wall()
            room_6.tiles[20][i].set_wall()
        room_6.tiles[8][self.room_size - 2].set_door(True)
        room_6.tiles[8][self.room_size - 2].set_door(False)
        room_6.tiles[12][2].set_door(True)
        room_6.tiles[12][2].set_door(False)
        room_6.tiles[16][self.room_size - 2].set_door(True)
        room_6.tiles[16][self.room_size - 2].set_door(False)
        room_6.tiles[20][2].set_door(True)
        room_6.tiles[20][2].set_door(False)

        switch_1 = Switch()
        switch_1.set_location(10, 12, room_6)
        switch_2 = Switch()
        switch_2.set_location(18, 12, room_6)

        room_6.tiles[self.room_size - 1][self.room_size - 3].set_door(True)

        room_6.tiles[5][0].set_door(True)
        room_6.tiles[5][0].set_door(False)
        self.add_rooms_to_room_arr(room_6)

    def room7(self):
        room_7 = Room(self.room_size, (0, 3))

        room_7.tiles[self.room_size - 1][12].set_door(True)
        room_7.tiles[self.room_size - 1][12].set_door(False)
        chest = Container()
        sling = Sling('sling')
        sign = Sign('"Try pressing ''Y''" he said.')
        room_7.tiles[19][4].set_sign(sign)
        chest.set_location(21, 2, room_7)
        chest.set_item(sling)

        i = 1
        k = 1
        while i < 23:
            k = 1
            while k < i:
                room_7.tiles[k][i].set_wall()
                k += 1
            i += 1

        self.add_rooms_to_room_arr(room_7)

    def room8(self):
        room_8 = Room(self.room_size, (1, 3))

        room_8.tiles[19][0].set_door(True)
        room_8.tiles[19][0].set_door(False)
        room_8.tiles[0][12].set_door(True)
        room_8.tiles[self.room_size - 1][22].set_door(True)

        for i in range(4, 16):
            for k in range(4, 20, 2):
                room_8.tiles[k][i].set_wall()

        switch_1 = Switch()
        switch_1.set_location(7, 10, room_8)
        switch_2 = Switch()
        switch_2.set_location(9, 10, room_8)
        switch_3 = Switch()
        switch_3.set_location(11, 10, room_8)
        switch_4 = Switch()
        switch_4.set_location(13, 10, room_8)
        switch_5 = Switch()
        switch_5.set_location(15, 10, room_8)

        self.add_rooms_to_room_arr(room_8)

    def room9(self):
        room_9 = Room(self.room_size, (2, 0))

        room_9.tiles[0][5].set_door(True)
        room_9.tiles[0][5].set_door(False)
        room_9.tiles[self.room_size - 1][5].set_door(True)
        room_9.tiles[self.room_size - 1][5].set_door(False)
        room_9.tiles[5][self.room_size - 1].set_door(True)

        for i in range(20, 2, -2):
            for j in range(20, i, -2):
                room_9.tiles[j][i].set_wall()

        self.add_rooms_to_room_arr(room_9)

    def room10(self):
        room_10 = Room(self.room_size, (2, 1))

        room_10.tiles[5][0].set_door(True)
        room_10.tiles[5][0].set_door(False)
        room_10.tiles[self.room_size - 1][18].set_door(True)
        room_10.tiles[self.room_size - 1][18].set_door(False)
        sign = Sign("WARNING!!! HOT LAVA AHEAD ")
        room_10.tiles[13][15].set_sign(sign)
        for i in range(4, 9):
            for k in range(4, 9):
                room_10.tiles[i][k].set_wall()
        for i in range(20, 23):
            for k in range(12, 15):
                room_10.tiles[i][k].set_wall()
        for i in range(15, self.room_size):
            room_10.tiles[i][17].set_wall()
            if i != 15:
                room_10.tiles[i][16].set_lava()
            room_10.tiles[i][15].set_wall()
            room_10.tiles[i][19].set_wall()
            if i != 15:
                room_10.tiles[i][20].set_lava()
            room_10.tiles[i][21].set_wall()
            room_10.tiles[i][22].set_wall()
        room_10.tiles[15][16].set_wall()
        room_10.tiles[15][20].set_wall()

        chest = Container()
        key_1 = Key("key")
        chest.set_location(4, 20, room_10)
        chest.set_item(key_1)
        self.add_rooms_to_room_arr(room_10)

    def room11(self):
        room_11 = Room(self.room_size, (2, 2))

        room_11.tiles[self.room_size - 1][10].set_door(True)
        room_11.tiles[self.room_size - 1][10].set_door(False)
        room_11.tiles[0][20].set_door(True)
        room_11.tiles[19][self.room_size - 1].set_door(True)
        room_11.tiles[19][self.room_size - 1].set_door(False)
        room_11.tiles[self.room_size - 1][20].set_door(True)
        room_11.tiles[self.room_size - 1][20].set_door(False)
        for i in range(16, self.room_size):
            room_11.tiles[i][18].set_wall()

        for i in range(18, self.room_size):
            room_11.tiles[16][i].set_wall()

        chest = Container()
        key = Key("key")
        chest.set_location(19, 1, room_11)
        chest.set_item(key)

        chest_2 = Container()
        coin_1 = Coin("coin", 2)
        chest_2.set_location(18, 1, room_11)
        chest_2.set_item(coin_1)

        chest_3 = Container()
        coin_2 = Coin("coin", 4)
        chest_3.set_location(20, 1, room_11)
        chest_3.set_item(coin_2)

        chest_4 = Container()
        coin_3 = Coin("coin", 4)
        chest_4.set_location(21, 1, room_11)
        chest_4.set_item(coin_3)

        room_11.tiles[22][1].set_wall()

        room_11.tiles[17][1].set_wall()

        for i in range(0, 17):
            for j in range(0, i + 1):
                room_11.tiles[i][j].set_wall()

        self.add_rooms_to_room_arr(room_11)

    def room12(self):
        room_12 = Room(self.room_size, (2, 3))

        room_12.tiles[0][22].set_door(True)
        room_12.tiles[0][22].set_door(False)

        room_12.tiles[19][0].set_door(True)

        for i in range(1, self.room_size - 5):
            room_12.tiles[8][i].set_wall()

        for i in range(1, self.room_size - 5):
            room_12.tiles[16][i].set_wall()

        sign = Sign("A distant target beckons")
        room_12.tiles[7][self.room_size - 4].set_sign(sign)

        target_1 = Target()
        target_1.set_location(12, 1, room_12)
        for i in range(9, 16):
            room_12.tiles[i][18].set_fence()

        self.add_rooms_to_room_arr(room_12)

    def room13(self):
        room_13 = Room(self.room_size, (3, 0))

        room_13.tiles[0][5].set_door(True)
        room_13.tiles[0][5].set_door(False)
        for i in range(4, self.room_size - 1):
            for k in range(1, 16):
                room_13.tiles[i][k].set_wall()
        chest = Container()
        key_1 = Key("key")
        chest.set_location(22, 20, room_13)
        chest.set_item(key_1)
        chest = Container()
        key_2 = Key("key")
        chest.set_location(22, 18, room_13)
        chest.set_item(key_2)
        chest_2 = Container()

        coin_2 = Coin("coin", 2)
        chest_2.set_location(22, 17, room_13)
        chest_2.set_item(coin_2)

        chest_3 = Container()
        coin_3 = Coin("coin", 4)
        chest_3.set_location(22, 19, room_13)
        chest_3.set_item(coin_3)

        chest_4 = Container()
        coin_4 = Coin("coin", 3)
        chest_4.set_location(22, 21, room_13)
        chest_4.set_item(coin_4)

        self.add_rooms_to_room_arr(room_13)

    def room14(self):
        room_14 = Room(self.room_size, (3, 1))

        room_14.tiles[0][18].set_door(True)
        room_14.tiles[0][18].set_door(False)
        room_14.tiles[18][self.room_size - 1].set_door(True)
        room_14.tiles[18][self.room_size - 1].set_door(False)
        for i in range(1, 23):
            for k in range(1, 23):
                if i != 1 or k != 18:
                    room_14.tiles[i][k].set_lava()

        self.add_rooms_to_room_arr(room_14)

    def room15(self):
        room_15 = Room(self.room_size, (3, 2))

        room_15.tiles[0][10].set_door(True)
        room_15.tiles[0][10].set_door(False)
        sign = Sign("This room could use some more signs")
        room_15.tiles[7][7].set_sign(sign)
        sign_2 = Sign("Hope you're enjoying your adventure!")
        room_15.tiles[14][17].set_sign(sign_2)
        room_15.tiles[18][0].set_door(True)
        room_15.tiles[18][0].set_door(False)
        room_15.tiles[0][20].set_door(True)
        room_15.tiles[0][20].set_door(False)
        room_15.tiles[18][self.room_size - 1].set_door(True)
        room_15.tiles[18][self.room_size - 1].set_door(False)

        for i in range(self.room_size):
            room_15.tiles[i][18].set_wall()

        j = 0
        for i in range(2, 12):
            j += 2
            for k in range(2, 12):
                room_15.tiles[j][i].set_wall()

        self.add_rooms_to_room_arr(room_15)

    def room16(self):
        room_16 = Room(self.room_size, (3, 3))
        winswitch = WinSwitch()
        winswitch.set_location(20, 20, room_16)
        winswitch.switch__on_off()
        for i in range(1, self.room_size - 1):
            for k in range(18, 22):
                winswitch.set_location(i, k, room_16)
                winswitch.switch__on_off()

        room_16.tiles[18][0].set_door(True)
        room_16.tiles[18][0].set_door(False)
        self.add_rooms_to_room_arr(room_16)

    """
    def count_wall_tiles(self): #testing method


        i=0
        for room in self.rooms_lst:
            for x in room.tiles:
                for y in x:
                    if y.is_wall_tile():
                        i+=1

            i=0
    """

    def get_adjacent_room(self, room, direction):

        original_coords = list(room.get_coordinates())
        adjacent_room_coords = list((None, None))
        adjacent_room_coords[0] = original_coords[0] + direction[0]
        adjacent_room_coords[1] = original_coords[1] + direction[1]
        adjacent_room_coords = tuple(adjacent_room_coords)

        return adjacent_room_coords

    def get_room_by_coords(self, coords):

        return self.room_arr[coords[0]][coords[1]]

    def outer_walls_for_room_switches(self):

        i = 0
        side = self.room_size
        for i in range(side):
            for k in range(side):
                if i == 0 or i == side - 1 or k == 0 or k == side - 1:
                    self.outer_walls.append((i, k))

            i += 1

    def opposite_door(self, x, y):

        if x == 0 or x == self.room_size - 1 or y == 0 or y == self.room_size - 1:

            if x == 0:
                x = self.room_size - 1
            elif x == self.room_size - 1:
                x = 0
            elif y == 0:
                y = self.room_size - 1
            elif y == self.room_size - 1:
                y = 0

            return (x, y)

        else:
            raise ValueError("Character not at edge of room")

    def add_rooms_to_room_arr(self, room_to_add):

        coords = room_to_add.get_coordinates()
        self.room_arr[coords[0]][coords[1]] = room_to_add

    def finish_line_coords(self):

        for i in range(1, self.room_size - 1):
            for k in range(18, 22):
                self.finish_line.append((i, k))

    def say_hey(self):
        print("hey hey hey")



