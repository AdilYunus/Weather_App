from scrapy.crawler import CrawlerProcess
from wiki.wiki.spiders.wiki_nl import WikiNlSpider
from wiki.wiki.spiders.wiki_us import WikiUsSpider
from wiki.wiki.spiders.wiki_tr import WikiTrSpider
from PyQt5 import QtWidgets, uic, QtCore,Qt
from PyQt5.QtCore import QTime, QTimer, Qt
import sys
import weather_app
import json
import loginres
import psycopg2
import os

conn = psycopg2.connect(database="Weather_App",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
cur = conn.cursor()

class Main(QtWidgets.QDialog):

    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('weatherUI/main.ui', self)
        #hidden frame -A
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #-display country in dropdown1 -A
        self.country_list = ['Netherlands','USA','Turkey']
        for i in self.country_list:
            self.selectCountry.addItem(i)
        #-----------------------------
        self.show()
        #----------------------------
        #database control
        self.control_dbase()
        #internet Control
        self.country_name =self.selectCountry.currentText()
        cur.execute(f"SELECT city_name from countries where country_name ='{self.country_name}' Order by population desc")
        cities = cur.fetchall()
        #----display cities in dropdown -A 
        for i in cities:
            self.selectCity.addItem(i[0])
        conn.commit()
        #-----select country--to display city -A
        self.selectCountry.activated[str].connect(self.display_city)
        #------select city --to display info -A
        self.selectCity.activated[str].connect(self.display_info)
        #----------------------------
        self.quit.clicked.connect(self.exit)
        #--timer pregress---
        self.count = 6 
        self.progressBar.setProperty("value",self.count)
        self.timer2 = QTimer(self)
        self.begin.clicked.connect(self.begin1)
        self.timer2.start(10)

        #----------------------
    def exit(self):
        conn.close()
        self.close()

    def display_info(self):
        self.city_name =self.selectCity.currentText()
        self.welcome.setText(f"Press Start to open weather information for ++{self.city_name}++")

    def timer_TimeOut(self):
        #methode for sleep time -A
        self.count += 1
        self.progressBar.setProperty("value",self.count)
        if self.count == 100:
            self.country_name=self.selectCountry.currentText()
            self.cams = weather_app.Weather_App(self.city_name,self.country_name)
            self.cams.show()
            self.close()
        
        conn.close()
    #begin and control internet -A
    def begin1(self):
        #control internet connection 
        exit_code = os.system('ping -n 1 www.google.com') 
        if exit_code ==1:
            self.welcome.setText("Please check your internet connection")
        else:
            self.display_info()
            self.timer2.timeout.connect(self.timer_TimeOut)

    #display city list in progress whet a country selecked -A
    def display_city(self,country):
        #qcombobox clear,
        self.selectCity.clear()
        # cur = conn.cursor()
        cur.execute(f"SELECT city_name from countries where country_name ='{country}' Order by population desc")
        cities = cur.fetchall()
        #----display cities in dropdown -A 
        for i in cities:
            # print(i)
            self.selectCity.addItem(i[0])
        conn.commit()
    
    def control_dbase(self):
        #control database 
        cur.execute("SELECT DISTINCT country_name FROM countries")
        all=cur.fetchall()

        if len(all) ==  0:
            # print("it is none")
            self.create_scrapy_information_db()

    def create_scrapy_information_db(self):
        #creat database via scrapy if there is not data -A
        process = CrawlerProcess()
        process.crawl(WikiUsSpider)
        process.crawl(WikiNlSpider)
        process.crawl(WikiTrSpider)
        process.start()

        

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
    window = Main()
    # window.show()
    # sys.exit(app.exec_())
    app.exec_()
