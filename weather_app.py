from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY
from PyQt5 import QtWidgets, uic, QtCore,Qt
from PyQt5.QtCore import QTime, QTimer, Qt, QDateTime,QDate
from PyQt5.QtGui import QPixmap, QIcon, QImage
import urllib3.request
import requests
import sys
import os
import json
import res
import psycopg2
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from wiki.wiki.spiders.wiki_nl import WikiNlSpider
from wiki.wiki.spiders.wiki_us import WikiUsSpider
from wiki.wiki.spiders.wiki_tr import WikiTrSpider
from PyQt5.QtGui import QPixmap, QImage
from datetime import datetime

conn = psycopg2.connect(database="Weather_App",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
cur = conn.cursor()

class Weather_App(QtWidgets.QDialog):

    def __init__(self,city_name,country_name):
        super(Weather_App,self).__init__()
        uic.loadUi('weatherUI/WeatherWithIcon.ui', self)
        #hidden frame -A
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.country_name= country_name
        self.city_name=city_name
        #-----------------------------
        # enter tusuyla da sonraki ikrana gidebilir -A
        self.search.setAutoDefault(True)
        #------------------------
        #-display country in dropdown1 -A
        country_list = ['Netherlands','USA','Turkey']
        for i in country_list:
            self.selectCountry.addItem(i)
        #--display country name from main page
        self.selectCountry.setCurrentText(self.country_name)
        #----display cities in dropdown -A 
        
        # self.selectCountry.currentText()
        cur.execute(f"SELECT city_name from countries where country_name ='{self.country_name}' Order by population desc")
        cities = cur.fetchall()
        #----display cities in dropdown -A 
        for i in cities:
            self.selectCity.addItem(i[0])
        conn.commit()
        self.selectCity.setCurrentText(self.city_name)
        #for showtime methode start timer
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        self.show()
        self.display_info()
        #-----------------------------
        self.get_api_now(self.city_name)
        # self.get_api_forecast()
        # self.prayer_times()
        #--------------------------
                #-----select country--to display city -A
        self.selectCountry.activated[str].connect(self.display_city)
        #------select city --to display info -A
        self.selectCity.activated[str].connect(self.display_info)
        #------quit button--A
        self.quit.clicked.connect(self.exit)
        #------------------------------
        self.city_name =city_name
        #call methode city_search when 1st open

        # self.city_search(self.city_name)
        # search box input
        self.search.clicked.connect(self.city_search) #when clicked go to methope city_search

    def exit(self):
        conn.close()
        self.close()
    #display informatie of select
    def display_info(self):
        self.error.clear()
        self.city_name =self.selectCity.currentText()
        cur.execute(f"SELECT city_name,province_name,population,country_name from countries where city_name ='{self.city_name}'")
        info = cur.fetchone()
        # print(info)
        self.infoData.setText(f": {info[0]}\n: {info[2]}\n: {info[1]}\n: {info[3]}")
        self.get_api_now(self.city_name)

    def display_Search_result(self,city_name):
        self.error.clear()
        cur.execute(f"SELECT city_name,province_name,population,country_name from countries where city_name ='{city_name}'")
        info = cur.fetchone()
        # print(info)
        self.infoData.setText(f": {info[0]}\n: {info[2]}\n: {info[1]}\n: {info[3]}")
        self.get_api_now(city_name)

    def display_city(self,country):
        #qcombobox clear,
        self.selectCity.clear()
        # cur = conn.cursor()
        cur.execute(f"SELECT city_name from countries where country_name ='{country}' Order by population desc")
        cities = cur.fetchall()
        #----display cities in dropdown -A 
        for i in cities:
            self.selectCity.addItem(i[0])
        conn.commit()
        
    def start(self):
        pass
        
    
    def get_api_now(self,city_name):
        try:
            apiKey = "fabf0da98fc2480e4a31f14c46f95389"
            origin_url="http://api.openweathermap.org/data/2.5/weather?"

            data= requests.get(origin_url)
            url= origin_url + "appid=" + apiKey + "&q=" + city_name       
            data = requests.get(url, params={
                "apikey":apiKey,
                "units":"metric"
                })
            global data_json
            data_json= data.json()
            


            temp= data_json["main"]["temp"]
            temp=int(temp)
            temp=str(temp)+"℃"
            description= data_json["weather"][0]["description"]
            country=data_json["sys"]["country"]
            icon=data_json["weather"][0]["icon"]
            

            url1= "http://openweathermap.org/img/wn/" 
            url2="@2x.png"
            url_icon= url1 + icon + url2
            
            res = requests.get(url_icon)
            img = QImage.fromData(res.content)

            self.bigcircul.setPixmap(QPixmap.fromImage(img))
            self.tempHour.setText(temp)
            self.tempHour1_2.setText(description)
        
            # print("temp: "+ str(float(temp)))
            # print("description:"+ str(description))
            # print("country:",country)
            # print("icon:",str(icon))

            
        except:
            print(f"Sorry,we have not info about {city_name}")
        self.get_api_forecast(city_name)
        self.prayer_times(city_name)

    def get_api_forecast(self,city_name):
        try:
            apiKey = "fabf0da98fc2480e4a31f14c46f95389" 
            lon=data_json['coord']['lon']
            lat=data_json['coord']['lat']
            url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apiKey}"
            response = requests.get(url, params={
                "apikey":apiKey,
                "units":"metric"
                })
            weather2 =response.json()
            list_icon=[]
            list_time=[]
            list_temp=[]
            for i in weather2['hourly'][2:10]:
                date=datetime.utcfromtimestamp(i['dt'])
                # print(str(date)[11:13])
                time=str(date)[11:13]
                list_time.append(time)
                #print(i['weather'][0]['description'])
                temp= i["temp"]
                temp=int(temp)
                temp=str(temp)+"℃"
                list_temp.append(temp)
                icon=i['weather'][0]['icon']
                # print(icon)
                list_icon.append(icon)
                



            # print(list_icon)
            url1 =f"http://openweathermap.org/img/wn/{list_icon[0]}@2x.png"
            res = requests.get(url1)
            img = QImage.fromData(res.content)
            self.circul1.setPixmap(QPixmap.fromImage(img))
            url2 =f"http://openweathermap.org/img/wn/{list_icon[1]}@2x.png"
            res = requests.get(url2)
            img = QImage.fromData(res.content)
            self.circul2.setPixmap(QPixmap.fromImage(img))
            url3 =f"http://openweathermap.org/img/wn/{list_icon[2]}@2x.png"
            res = requests.get(url3)
            img = QImage.fromData(res.content)
            self.circul3.setPixmap(QPixmap.fromImage(img))
            url4 =f"http://openweathermap.org/img/wn/{list_icon[3]}@2x.png"
            res = requests.get(url4)
            img = QImage.fromData(res.content)
            self.circul4.setPixmap(QPixmap.fromImage(img))
            url5 =f"http://openweathermap.org/img/wn/{list_icon[4]}@2x.png"
            res = requests.get(url5)
            img = QImage.fromData(res.content)
            self.circul5.setPixmap(QPixmap.fromImage(img))
            url6 =f"http://openweathermap.org/img/wn/{list_icon[5]}@2x.png"
            res = requests.get(url6)
            img = QImage.fromData(res.content)
            self.circul6.setPixmap(QPixmap.fromImage(img))
            url7 =f"http://openweathermap.org/img/wn/{list_icon[6]}@2x.png"
            res = requests.get(url7)
            img = QImage.fromData(res.content)
            self.circul7.setPixmap(QPixmap.fromImage(img))
            url8 =f"http://openweathermap.org/img/wn/{list_icon[7]}@2x.png"
            res = requests.get(url8)
            img = QImage.fromData(res.content)
            self.circul8.setPixmap(QPixmap.fromImage(img))
            ###########################################################################################
            self.saat1.setText(list_time[0])
            self.saat2.setText(list_time[1])
            self.saat3.setText(list_time[2])
            self.saat4.setText(list_time[3])
            self.saat5.setText(list_time[4])
            self.saat6.setText(list_time[5])
            self.saat7.setText(list_time[6])
            self.saat8.setText(list_time[7])

            self.tempHour1.setText(list_temp[0])
            self.tempHour2.setText(list_temp[1])
            self.tempHour3.setText(list_temp[2])
            self.tempHour4.setText(list_temp[3])
            self.tempHour5.setText(list_temp[4])
            self.tempHour6.setText(list_temp[5])
            self.tempHour7.setText(list_temp[6])
            self.tempHour8.setText(list_temp[7])


            # print("=============================================================================")
            list_temp_day=[]
            list_iconn=[]
            list_day=[]
            for i in weather2['daily'][1:6]:
                date=datetime.utcfromtimestamp(i['dt'])
                day=str(date)[5:10]
                list_day.append(day)
                #print(i['weather'][0]['description'])
                iconn=i['weather'][0]['icon']
                list_iconn.append(iconn)

                temp_min= i["temp"]['min']
                temp_min=int(temp_min)
                temp_min=str(temp_min)
                temp_max= i["temp"]['max']
                temp_max=int(temp_max)
                temp_max=str(temp_max)+"℃"
                list_temp_day.append(temp_min+'~'+temp_max)
            ##############################################################################################
            self.tempweek1.setText(list_temp_day[0])
            self.tempweek2.setText(list_temp_day[1])
            self.tempweek3.setText(list_temp_day[2])
            self.tempweek4.setText(list_temp_day[3])
            self.tempweek5.setText(list_temp_day[4])

            self.weekName1.setText(list_day[0])
            self.weekName2.setText(list_day[1])
            self.weekName3.setText(list_day[2])
            self.weekName4.setText(list_day[3])
            self.weekName5.setText(list_day[4])
            

            url1 =f"http://openweathermap.org/img/wn/{list_iconn[0]}@2x.png"
            res = requests.get(url1)
            img = QImage.fromData(res.content)
            self.smalcircul1.setPixmap(QPixmap.fromImage(img))
            url2=f"http://openweathermap.org/img/wn/{list_iconn[1]}@2x.png"
            res = requests.get(url2)
            img = QImage.fromData(res.content)
            self.smalcircul2.setPixmap(QPixmap.fromImage(img))
            url3=f"http://openweathermap.org/img/wn/{list_icon[2]}@2x.png"
            res = requests.get(url3)
            img = QImage.fromData(res.content)
            self.smalcircul3.setPixmap(QPixmap.fromImage(img))
            url4=f"http://openweathermap.org/img/wn/{list_icon[3]}@2x.png"
            res = requests.get(url4)
            img = QImage.fromData(res.content)
            self.smalcircul4.setPixmap(QPixmap.fromImage(img))
            url5=f"http://openweathermap.org/img/wn/{list_icon[4]}@2x.png"
            res = requests.get(url5)
            img = QImage.fromData(res.content)
            self.smalcircul5.setPixmap(QPixmap.fromImage(img))




            # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        except:
            print(f"Sorry,we have not info about {city_name}")

    def prayer_times(self,city_name):
        datetime1 = QDateTime.currentDateTime()
        today =datetime1.toString("dd-MM-yyyy")
        # try:
        #     url = "https://dailyprayer.abdulrcs.repl.co/api/"+city_name
        #     print(url)
        #     response = requests.get(url)
        #     data = response.json()

        #     list_prayer=[]
        #     for prayer in data["today"]: 
        #         prayer=str(prayer)
        #         prayer_date= data["today"][prayer] 
        #         prayer_date=str(prayer_date)
        #         list_prayer.append(prayer+'--'+prayer_date)
                

        #     ######################################################
        #     self.pray1.setText(list_prayer[0])
        #     self.pray2.setText(list_prayer[1])
        #     self.pray3.setText(list_prayer[2])
        #     self.pray4.setText(list_prayer[3])
        #     self.pray5.setText(list_prayer[4])
        #     self.pray6.setText(list_prayer[5])
        
        # except:
        #     print(f"Sorry,we have not prayer time info about {city_name}")

        
        url = f"https://api.aladhan.com/v1/timingsByAddress/{today}?address={self.city_name}&method=8"
        try:
            response = requests.get(url)
            data = response.json()
            self.pray1.setText('Fajr -- '+data["data"]['timings']['Fajr'])
            self.pray2.setText('Sunrise -- '+data["data"]['timings']['Sunrise'])
            self.pray3.setText('Dhuhr -- '+data["data"]['timings']['Dhuhr'])
            self.pray4.setText('Asr -- '+data["data"]['timings']['Asr'])
            self.pray5.setText('Maghrib -- '+data["data"]['timings']['Maghrib'])
            self.pray6.setText('Isha --'+data["data"]['timings']['Isha'])
            self.pray7.setText('Hijri : '+data["data"]['date']['hijri']['date'])
            
        except:
            print("Sorry,we have not info about {city_name}")

    def city_control_dbase(self,city_name):
        pass
    
    def create_scrapy_information_db(self):
        process = CrawlerProcess()
        process.crawl(WikiUsSpider)
        process.crawl(WikiNlSpider)
        process.crawl(WikiTrSpider)
        process.start()


    def city_search(self):
        self.city_name = self.searchBox.text().title()
        conn = psycopg2.connect(database="Weather_App",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()

        cur.execute(f"SELECT city_name from countries WHERE city_name = '{self.city_name}' ")
        city = cur.fetchone()
        # print(city)
        if city:
            self.get_api_now(self.city_name)
            self.get_api_forecast(self.city_name)
            self.prayer_times(self.city_name)
            self.display_Search_result(self.city_name)

        else:
            self.infoData.clear()
            self.error.setText(f"Sorry,there is no information about {self.city_name}")


    
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
    #Show correntTime methode   
    def showtime(self):
        # now = QDate.currentDate()
        datetime = QDateTime.currentDateTime()
        text1=datetime.toString("dddd , dd  MMMM  yyyy")
        text2 = datetime.toString(" hh:mm:ss")
        self.timeShow1.setText(text1)
        self.timeShow2.setText(text2)
        today =datetime.toString("dd-MM-yyyy")
    #--------------------------------------


# if __name__ == "__main__":
#     app =  QtWidgets.QApplication(sys.argv)
#     window = Weather_App()
#     app.exec_()
