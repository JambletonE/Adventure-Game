class WinSwitch:

    def __init__(self):
        self.is_on = False
        self.location = None


    def switch__on_off(self):

        if self.is_on:

            self.is_on = False
        else:
            self.is_on = True

    def get_is_on(self):

        return self.is_on

    def set_location(self, column, row, room):#
        if room.tiles[column][row].is_empty():
            self.location=(column, row)
            room.set_win_switch(column, row, self)

    def get_location(self):


        return self.location

