import sys
from time import sleep

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ServerChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())


class GameServer(Server):
    channelClass = ServerChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = {}
        print('Server started')

    def NextId(self):
        self.id += 1
        return self.id
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = True
        player.Send({"action": "initial", 'message':'Pryvit Anton'})
        #self.SendPlayers()

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = GameServer(localaddr=(host, int(port)))
    s.Launch()