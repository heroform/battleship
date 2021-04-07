from abc import ABC, abstractmethod

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
            success = canPlaceShipHere(x, y, direction)
            if not success:
                self.printError('Invalid ship\'s position.')

    @abstractmethod
    def canPlaceShipHere(x, y, direction):
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