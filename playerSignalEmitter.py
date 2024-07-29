from PyQt5.QtCore import QObject, pyqtSignal
class playerSignalEmitter(QObject):
    playerSignal = pyqtSignal(list)