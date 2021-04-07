import getopt, sys
from bs_client import BattleShipClient

arguments = sys.argv[1:]

shortOptions = 'h:p:ivc:'
longOptions = ['host', 'port', 'interact', 'verbose', 'captain']

try:
    arguments, values = getopt.getopt(arguments, shortOptions, longOptions)
except getopt.error as err:
    print (str(err))
    sys.exit(2)

interact = False
verbose = False

for arg, val in arguments:
    if arg in ('-h', '--host'):
        host = val
    elif arg in ('-p', '--port'):
        port = val
    elif arg in ('-i', '--interact'):
        interact = True
    elif arg in ('-v', '--verbose'):
        verbose = True
    elif arg in ('-c', '--captain'):
        captain = val

port = int(port)

client = BattleShipClient(captain, host, port, interact, verbose)
client.start()