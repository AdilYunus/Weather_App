from PyQt5 import QtWidgets, uic, QtCore,Qt
from PyQt5.QtCore import QTime, QTimer, Qt
import sys
import weather_app
import json
import loginres

class Main(QtWidgets.QDialog):

    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('weatherUI/main.ui', self)
        #hidden frame -A
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #-----------------------------

        self.show()
        self.quit.clicked.connect(self.close)
        self.count = 6 
        self.progressBar.setProperty("value",self.count)
        self.timer2 = QTimer(self)
        self.begin.clicked.connect(self.begin1)
        self.timer2.start(5)

    def timer_TimeOut(self):
        #methode for sleep time 
        self.count += 1
        self.progressBar.setProperty("value",self.count)
        if self.count == 100:
        
            self.cams = weather_app.Weather_App()
            self.cams.show()
            self.close()
    def begin1(self):
        self.timer2.timeout.connect(self.timer_TimeOut)


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
