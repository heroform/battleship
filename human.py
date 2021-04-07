from player_starter import Player


class Human(Player):
    def __init__(self, name, longtitude, latitude, direction):
        super(Human, self).__init__(name)
        self.ship_size = 3
        self.board = numpy.zeros([8, 8], dtype=int)

    def choosePosition(self):
        print('Enter the coordination:')
        x = input('x: ')
        y = input('y: ')
        if not x.isnumeric() or not y.isnumeric():
            print('Your coordinate is not the number!')
        direction = input('Enter the direction (up, down, left, right): ')
        return int(x), int(y), direction

    def canPlaceShipHere(self, x, y, direction):
        if x - self.ship_size < 0:
            if direction == 'up':
                return False
        elif x + self.ship_size > 7:
            if direction == 'down':
                return False
        elif y - self.ship_size < 0:
            if direction == 'right':
                return False
        elif y + self.ship_size > 7:
            if direction == 'left':
                return False
        return True
