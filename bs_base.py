BUFFER_SIZE = 1024
class BattleShipBase:
    def __init__(self, host='127.0.0.1', port=54321, interact=False, verbose=False):
        self._host = host
        self._port = port
        self._interact = interact
        self._verbose = verbose


    def receiveShotInfo(self, conn):
        info = self.receiveMessage(conn)
        info = info.split(' ')
        info = list(map(int, info))
        return info[0], info[1]

    def sendShotInfo(self, conn, x, y):
        info = '{0} {1}'.format(x, y)
        self.sendMessage(conn, info)

    def sendMessage(self, conn, msg):
        whites = ' ' * (BUFFER_SIZE - len(msg))
        msg += whites
        conn.send(msg.encode('utf8'))

    def receiveMessage(self, conn):
        msg = conn.recv(BUFFER_SIZE).decode('utf8').strip()
        return msg

    def debug__verbose(self, *messages):
        if not self._verbose:
            return
        for msg in messages:
            print(msg)
        if self._interact:
            input('Press any key to continue...')