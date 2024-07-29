import time
from threading import Thread
from APIHelper import APIhelper
import json
import getpass
class ChatFetcher:
    latestMsg = None
    running = False;
    chatPrefix = "[Client thread/INFO]: [CHAT]"
    onlinePrefix = "ONLINE: "
    quitPrefix = "has quit!"
    joinPrefix = "has joined"
    config = open('config.json', 'r').read()
    config_json = json.loads(config)
    HypixelAPI1 = config_json["HypixelAPI1"]
    def follow(self, thefile):
        thefile.seek(0, 2)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def __init__(self, delegate):
        self.delegate = delegate
        listenThread = Thread(target = self.listen,args=())
        listenThread.start()


    def addPlayer(self, IGN):
        self.delegate.appendPlayer([IGN])
    def clearPlayerList(self):
        self.delegate.clearPlayerStatsDisplay()
    def removePlayer(self, IGN):
        self.delegate.removePlayer(IGN)
    def listen(self):
        try:
            localUserName = getpass.getuser()
            print(localUserName)
            logFile = open(rf"C:\Users\{localUserName}\.lunarclient\offline\multiver\logs\latest.log", "r")
            loglines = self.follow(logFile)
            for line in loglines:
                print(line)
                if line[11:39] == self.chatPrefix:
                    if len(line) > 48:
                        if line[40:48] == self.onlinePrefix:
                            print(line[48:])
                            playerList = line[48:-1].split(", ")
                            self.delegate.whoStats(playerList)
                            """
                            for player in playerList:
                                self.addPlayer(player)
                                t1 = Thread(target=self.delegate.queryStats, args=[player])
                                t1.start()
                                """
                    if line[-10:-1] == self.quitPrefix:
                        player = line[40:-11]
                        self.removePlayer(player)
                        #print(player)
                    elif line[-19:-9] == self.joinPrefix or line[-18:-8] == self.joinPrefix or line[-20:-10] == self.joinPrefix:
                        line1 = line[40:]
                        player =  line1[:line1.find(" ")]
                        self.addPlayer(player)
                        t1 = Thread(target=self.delegate.queryStats, args=[player])
                        t1.start()
        except Exception as e:
            print(e)

    #def getMessage:
