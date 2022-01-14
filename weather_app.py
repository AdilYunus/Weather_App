from PyQt5 import QtWidgets, uic, QtCore,Qt
from PyQt5.QtCore import QTime, QTimer, Qt
import sys
import os
import json
import res


class Weather_App(QtWidgets.QDialog):

    def __init__(self):
        super(Weather_App,self).__init__()
        uic.loadUi('weatherUI/WeatherWithIcon.ui', self)
        #hidden frame -A
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #-----------------------------
        # enter tusuyla da sonraki ikrana gidebilir -A
        self.search.setAutoDefault(True)
        #------------------------
        self.show()
        #------quit button--A
        self.quit.clicked.connect(self.close)

        
    def start(self):
        pass
        
    
    def get_api_now(self):
        pass

    def get_api_8_hour(self):
        pass

    def prayer_times(self):
        pass

    def city_control_dbase(self):
        pass
    
    def create_scrapy_information_db(self):
        pass

    def city_search(self):
        pass
    
    #windows moving without frame---A
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ismoving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if self.ismoving:
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos) 
    def mouseReleaseEvent(self, e):
        self.ismoving = False
    #-----------------------------------



if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = Weather_App()
    app.exec_()
