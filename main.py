import sys
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication
from gui import GUI
from room import Room
from container import Container
from key import Key
from coin import Coin
from player import Player
from enemy import Enemy
from sign import Sign



def main():

    ########################### Starting Room ####################################
    """
    This first room was used as a test chamber for features that were later
    deployed to other rooms it was easiest to keep it here in the main.py for
    development purposes.

    """
    room_size=24
    room = Room(room_size, (1, 1)) #creates room size 24 at coordinates (1, 1)

    #Create enemy and player and set there start locations
    player = Player()
    enemy = Enemy(10) #create enemy with power
    player.set_location(12,12,room)
    enemy.set_location(2,2,room)

    # Creates a sign and sets the position
    sign_1= Sign("You need a key to unlock the door")
    room.tiles[16][15].set_sign(sign_1)

    # Creates some doors and internal walls

    room.tiles[12][0].set_door(True)
    room.tiles[12][10].set_door(True)

    for i in range(room_size):
        room.tiles[i][10].set_wall()

    for i in range(8):
        room.tiles[i][7].set_wall()
        room.tiles[7][i].set_wall()


    # The below method of creating a door and setting it to false
    # is a simple way of creating a gap in a wall.
    room.tiles[4][7].set_door(True)
    room.tiles[4][7].set_door(False)
    room.tiles[0][8].set_door(True)
    room.tiles[0][8].set_door(False)

    # Creates a chest and sets location
    chest = Container()
    chest.set_location(12,20,room)

    # Creates a key and places it inside the chest
    key_1 = Key("key")
    chest.set_item(key_1)

    # Creates a second chest
    chest_2 = Container()
    chest_2.set_location(20, 4, room)

    # Creates a coin of value 5 and puts it in the
    # second chest.
    coin_1 = Coin("coin", 5)
    chest_2.set_item(coin_1)

    # Creates  horizontal lines of wall tiles.

    for i in range(room_size):
        if i % 2 == 0:
            room.tiles[i][21].set_wall()
        room.tiles[i][22].set_wall()

    ######################################################################3



    global app
    app = QApplication(sys.argv)
    tile_size=25
    gui = GUI(room, tile_size,player,enemy)


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()