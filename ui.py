from PyQt5 import QtCore, QtGui, QtWidgets
from UIDelegate import UIDelegate
from playerSignalEmitter import playerSignalEmitter
from ChatFetcher import ChatFetcher
from APIHelper import APIhelper

from threading import *
import concurrent.futures
import json
from functools import partial
class Ui_MainWindow(UIDelegate):
    bot = None
    mapPrefix = "You are currently playing on "
    config = open('config.json', 'r').read()
    config_json = json.loads(config)
    HypixelAPI1 = config_json["HypixelAPI1"]
    HypixelAPI2 = config_json["HypixelAPI2"]
    headers = config_json["headers"]
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 860)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.statsDisplay = QtWidgets.QTableView(self.centralwidget)
        self.statsDisplay.setGeometry(QtCore.QRect(10, 10, 1000, 831))
        self.statsDisplay.setObjectName("statsDisplay")
        self.statsModel = QtGui.QStandardItemModel()
        self.statsDisplay.setModel(self.statsModel)
        self.statsModel.setHorizontalHeaderLabels(self.headers)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.playerSignalEmitter = playerSignalEmitter()
        self.playerSignalEmitter.playerSignal.connect(self.appendPlayerStats)
        #self.playerSignalEmitter.playerSignal.emit(["lmao"])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


    def appendPlayerStats(self, stats):
        print(stats)
        name = stats[0]
        for row in range(self.statsModel.rowCount()):
            item = self.statsModel.item(row,0)

            if item is not None and item.text() == name:
                for column in range(len(stats)):
                    curitem = QtGui.QStandardItem(str(stats[column]))
                    if stats[1] == ('Nick') or int(stats[2] or -1) > 934 or int(stats[3] or -1) >= 15 or int(stats[4] or -1) >= 10:
                        curitem.setBackground(QtGui.QColor(188,143,228,250))
                    try:
                        self.statsModel.setItem(row, column, curitem)
                    except Exception as e:
                        print(e)
    def appendPlayer(self, stats):
        curPlayerList = []
        for row in range(self.statsModel.rowCount()):
            curPlayerList.append(self.statsModel.item(row, 0).text())
        if stats[0] not in curPlayerList:
            while len(stats) < 6:
                stats.append("")
            print(stats)
            row_items = [QtGui.QStandardItem(str(item)) for item in stats]
            self.statsModel.appendRow(row_items)

    def removePlayer(self, username):
        for row in range(self.statsModel.rowCount()):
            item = self.statsModel.item(row, 0)
            if item is not None and item.text() == username:
                self.statsModel.removeRow(row)
                break;
    def clearPlayerStatsDisplay(self):
        self.statsModel.removeRows(0,self.statsModel.rowCount())
    def whoStats(self, playerList):
        curPlayerList = []
        for row in range(self.statsModel.rowCount()):
           curPlayerList.append(self.statsModel.item(row,0).text())
        for newPlayer in playerList:
            if newPlayer not in curPlayerList:
                self.appendPlayer([newPlayer])
                t1 = Thread(target=self.queryStats, args=[newPlayer])
                t1.start()
        for existPlayer in curPlayerList:
            if existPlayer not in playerList:
                self.removePlayer(existPlayer)
    def queryStats(self, playerIGN):
        data = None
        try:
            data = APIhelper.query(playerIGN, self.HypixelAPI1)
        except Exception as e:
            print(e)
            data = [playerIGN, 'Nick']
        if data != None:
            self.playerSignalEmitter.playerSignal.emit(data)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.chatFetcher = ChatFetcher(ui)
    sys.exit(app.exec_())