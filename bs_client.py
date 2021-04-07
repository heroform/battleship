import socket
from bs_base import BattleShipBase
from player_starter import GodCom

class BattleShipClient(BattleShipBase):
    def __init__(self, playerName, host='127.0.0.1', port=54321, interact=False, verbose=False):
        super().__init__(host, port, interact, verbose)
        self.__player = GodCom(playerName)
        self.__player.placeShips()

        if verbose:
            self.__player.showBoard()

        self.__socket = None

    def start(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self._host, self._port))
            self.debug__verbose('Connected to {0}:{1}'.format(self._host, self._port))

            self.sendMessage(self.__socket, self.__player.name)
            self.playAGame()
        except ConnectionRefusedError:
            print('Cannot connect to {0}:{1}'.format(self._host, self._port))

    def keepShooting(self):
        keepShooting = True
        isOver = False
        while keepShooting:
            x, y = self.__player.shot()
            self.debug__verbose('Shot at ({0}, {1})'.format(x, y))
            self.sendShotInfo(self.__socket, x, y)
            command = self.receiveMessage(self.__socket)
            self.debug__verbose(command)
            if self._verbose:
                self.__player.showBoard()
            isOver = command == 'over'
            keepShooting = not isOver and command == 'hit'
        return isOver

    def keepBingShot(self):
        keepBeingShot = True
        isOver = False
        while keepBeingShot:
            x, y = self.receiveShotInfo(self.__socket)
            self.debug__verbose('Got shot at ({0}, {1})'.format(x, y))

            self.sendShotResult(x, y)
            command = self.receiveMessage(self.__socket)

            self.debug__verbose(command)
            if self._verbose:
                self.__player.showBoard()

            isOver = command == 'over'
            keepBeingShot = not isOver and command == 'hit'
        return isOver

    def playAGame(self):
        isOver = False
        while not isOver:
            playerOrder = self.receiveMessage(self.__socket)
            if playerOrder == 'first':
                isOver = self.keepShooting()
            else:
                isOver = self.keepBingShot()

        if self.__player.isLost():
            print('You loose!')
        else:
            print('You win!')
            self.sendMessage(self.__socket, str(self.__player.score))

    def sendShotResult(self, x, y):
        hit = self.__player.getShot(x, y)
        lost = self.__player.isLost()
        info = '{0} {1}'.format(hit, lost)
        self.sendMessage(self.__socket, info)

