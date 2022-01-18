from PyQt5 import QtWidgets, uic, QtCore,Qt
from PyQt5.QtCore import QTime, QTimer, Qt, QDateTime,QDate
from PyQt5.QtGui import QPixmap, QImage 
import sys
import os
import json
import res
import requests
from requests.models import Response
import json
from datetime import datetime


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
        #for showtime methode start timer
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        self.show()
        #--------------------------
        #------quit button--A
        self.quit.clicked.connect(self.close)

        url = "http://openweathermap.org/img/wn/10d@2x.png"

        res = requests.get(url)
        img = QImage.fromData(res.content)
        # corrent 
        #self.bigcircul.setPixmap(QPixmap.fromImage(img))
        self.get_api_now()
        self.get_api_forecast()
        self.prayer_times()
        
    def start(self):
        pass
        
    
    def get_api_now(self):
        try:
            apiKey = "fabf0da98fc2480e4a31f14c46f95389"
            origin_url="http://api.openweathermap.org/data/2.5/weather?"

            # city_name =input("enter your city: ")
            global city_name
            city_name= "Hawaii"
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
            icon="04n"
            url_icon= url1 + icon + url2
            # url_icon= url1 + icon + url2
            # print(url_icon)
            
            res = requests.get(url_icon)
            img = QImage.fromData(res.content)

            self.bigcircul.setPixmap(QPixmap.fromImage(img))
            self.tempHour.setText(temp)
            self.tempHour1_2.setText(description)
        
            print("temp: "+ str(float(temp)))
            print("description:"+ str(description))
            print("country:",country)
            print("icon:",str(icon))

            
        except:
            print(f"Sorry,we have not info about {city_name}")
        
    def get_api_forecast(self):
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
                print(str(date)[11:13])
                time=str(date)[11:13]
                list_time.append(time)
                #print(i['weather'][0]['description'])
                temp= i["temp"]
                temp=int(temp)
                temp=str(temp)+"℃"
                list_temp.append(temp)
                icon=i['weather'][0]['icon']
                print(icon)
                list_icon.append(icon)
                



            print(list_icon)
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


            print("=============================================================================")
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




            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        except:
            print(f"Sorry,we have not info about {city_name}")
        

    def prayer_times(self):
        try:
            url = "https://dailyprayer.abdulrcs.repl.co/api/"+city_name
            response = requests.get(url)
            data = response.json()
            #print(data['city'])
            print(data['date'])
            list_prayer=[]
            for prayer in data["today"]: 
                prayer=str(prayer)
                prayer_date= data["today"][prayer] 
                prayer_date=str(prayer_date)
                list_prayer.append(prayer+'--'+prayer_date)
            print(list_prayer)
            print("====================================================")

            ######################################################
            self.pray1.setText(list_prayer[0])
            self.pray2.setText(list_prayer[1])
            self.pray3.setText(list_prayer[2])
            self.pray4.setText(list_prayer[3])
            self.pray5.setText(list_prayer[4])
            self.pray6.setText(list_prayer[5])
        
        except:
            print(f"Sorry,we have not info about {city_name}")
        
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
    #Show correntTime methode   
    def showtime(self):
        # now = QDate.currentDate()
        datetime = QDateTime.currentDateTime()
        text1=datetime.toString("dddd , dd  MMMM  yyyy")
        text2 = datetime.toString(" hh:mm:ss")
        self.timeShow1.setText(text1)
        self.timeShow2.setText(text2)
    #--------------------------------------


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = Weather_App()
    app.exec_()

#window.get_api_now()
#window.get_api_8_hour()
#window.prayer_times()
