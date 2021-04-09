from abc import ABC, abstractmethod
import random
import numpy

NSHIPS = 3
class Player(ABC):
    def __init__(self, name):
        self._name = name
        self._score = 0
        # TODO: init your board

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    def placeShips(self):
        for i in range(NSHIPS):
            self.placeAShip()

    @abstractmethod
    def choosePosition(self):
        # TODO: override this method to return x, y, direction
        pass

    def printError(self, msg):
        print(msg)

    def placeAShip(self):
        success = False
        while not success:
            x, y, direction = self.choosePosition()
            success = self.canPlaceShipHere(x, y, direction)
            if not success:
                self.printError('Invalid ship\'s position.')

    @abstractmethod
    def canPlaceShipHere(self, x, y, direction):
        # TODO: check if you can place a ship on your board with x, y, direction
        # Note: check if your ship is over board or not, 
        #       check if your ships are overlapped or not
        # Update: if you can, place a ship and return True, otherwise return False
        pass
    
    def shot(self):
        self._score += 1
        # TODO: You should override this method to return a shoot (x, y)
        return 0, 0

    @abstractmethod
    def getShot(self, x, y):
        # TODO: You should override this method to check if a shot (x, y) hits one of your
        # ships. Also if it hits, change the cell value at (x, y) to -1
        pass

    @abstractmethod
    def isLost(self):
        # TODO: check if all of your ships are burnt
        pass

    def showBoard(self):
        print('BOARD of', self._name)
        # TODO: print your board information
        
class GodCom(Player):
    def __init__(self, name):
        super().__init__(name)
        self.ship_size = 3
        self.board = numpy.zeros([8, 8], dtype=int)
        self.end_turn = False
        self.valid_shot = True

    def choosePosition(self):
        positions = ['up', 'down', 'left', 'right']
        x, y = (random.randint(0, 7), random.randint(0, 7))
        position = random.choice(positions)
        return x, y, position
        
    def canPlaceShipHere(self, x, y, direction):
        if direction == 'up':
            if x + self.ship_size > 7:  # Check outside of board
                return False
            else:
                for i in range(self.ship_size):
                    if self.board[x + i][y] == 1:  # Check overlap
                        return False
                for i in range(self.ship_size):  # Place ship
                    self.board[x + i][y] = 1
                return True

        if direction == 'down':
            if x - self.ship_size < 0:
                return False
            else:
                for i in range(self.ship_size):
                    if self.board[x - i][y] == 1:
                        return False
                for i in range(self.ship_size):
                    self.board[x - i][y] = 1
                return True

        if direction == 'right':
            if y - self.ship_size < 0:
                return False
            else:
                for i in range(self.ship_size):
                    if self.board[x][y - i] == 1:
                        return False
                for i in range(self.ship_size):
                    self.board[x][y - i] = 1
                return True

        if direction == 'left':
            if y + self.ship_size > 7:
                return False
            else:
                for i in range(self.ship_size):
                    if self.board[x][y + i] == 1:
                        return False
                for i in range(self.ship_size):
                    self.board[x][y + i] = 1
                return True

        return False

    def shot(self):
        self._score += 1
        self.end_turn = False
        self.valid_shot = True
        return random.randint(0, 7), random.randint(0, 7)

    def getShot(self, x, y):
        if self.isLost():  # Check if finished
            self.end_turn = True
            self._score -= 1
            return True

        if self.board[x][y] == 1:
            self.board[x][y] = -1
            print("{}: Huhu! You sank my battleship!".format(self.name))
            self.end_turn = False  # Keep shooting
            self.valid_shot = True
            return True
        else:
            if x not in range(8) or y not in range(8):
                print("{}: You traveled so far, not in the board! Choose again!".format(self.name))
                self.valid_shot = False  # Return previous score
                self.end_turn = False  # Choose again
            elif self.board[x][y] == -1:
                print("{}: You guessed that one already!".format(self.name))
                self.valid_shot = False
                self.end_turn = False  # Choose again
            else:
                print("{}: How can you missed? LOL!".format(self.name))
                self.board[x][y] = -1
                self.end_turn = True  # End turn
                print(self.board)
            return False

    def isLost(self):
        if 1 not in self.board:
            return True
        else:
            return False
        
    def showBoard(self):
        print(self.board)

    def showScore(self):
        print('{}\'s score: {}'.format(self.name, self._score))

    def roll_back_score(self):
        self._score -= 1


class Human(Player):
    def __init__(self, name):
        super(Human, self).__init__(name)
        self.ship_size = 3
        self.board = numpy.zeros([8, 8], dtype=int)
        self.end_turn = False

    def choosePosition(self):
        print('Enter the coordination:')
        x = input('x: ')
        y = input('y: ')
        if not x.isnumeric() or not y.isnumeric():
            print('Your coordinate is not the number!')
        direction = input('Enter the direction (up, down, left, right): ')
        return int(x), int(y), direction

    def canPlaceShipHere(self, x, y, direction):
        if direction == 'up':
            if x - self.ship_size < 0:
                return False
            else:
                for i in range(self.ship_size):
                    self.board[x + i][y] = 1
                return True

        if direction == 'down':
            if x + self.ship_size > 7:
                return False
            else:
                for i in range(self.ship_size):
                    self.board[x - i][y] = 1
                return True

        if direction == 'right':
            if y - self.ship_size < 0:
                return False
            else:
                for i in range(self.ship_size):
                    self.board[x][y - i] = 1
                return True

        if direction == 'left':
            if y + self.ship_size > 7:
                return False
            else:
                for i in range(self.ship_size):
                    self.board[x][y + i] = 1
                return True

        return False

    def shot(self):
        self._score += 1
        return random.randint(0, 7), random.randint(0, 7)

    def getShot(self, x, y):
        if self.board[x][y] == 1:
            self.board[x][y] = -1
            print("Huhu! You sank my battleship!")
            self.end_turn = False
            return True
        else:
            if x not in range(8) or y not in range(8):
                print("You traveled so far, not in the board! Choose again!")
                self.end_turn = False
            elif self.board[x][y] == -1:
                print("You guessed that one already!")
                self.end_turn = False
            else:
                print("How can you missed? LOL!")
                self.board[x][y] = -1
                self.end_turn = True
                print(self.board)
            return False

    def isLost(self):
        if 1 not in self.board:
            return True
        else:
            return False

    def showBoard(self):
        print(self.board)



if __name__ == '__main__':
    god = GodCom('God')
    human = GodCom('Human')
    god.placeShips()
    god.showBoard()
    human.placeShips()
    human.showBoard()

    limit = 100
    n = 0

    while True:
        while not human.end_turn:
            x1, y1 = god.shot()
            human.getShot(x1, y1)
            if not human.valid_shot:
                god.roll_back_score()
        if human.isLost():
            print("{} win!".format(god.name))
            break

        while not god.end_turn:
            x2, y2 = human.shot()
            god.getShot(x2, y2)
            if not god.valid_shot:
                human.roll_back_score()
        if god.isLost():
            print("{} win!".format(human.name))
            break

    god.showScore()
    human.showScore()

