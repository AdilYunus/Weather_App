from urllib.parse import urlunparse
import scrapy
import psycopg2

conn = psycopg2.connect(database="Weather_App",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
cur = conn.cursor()

class WikiNlSpider(scrapy.Spider):
    name = 'wiki_nl'
    # allowed_domains = ['nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen_met_stadsrechten']
    start_urls = ['https://nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen_met_stadsrechten']
    custom_setting = {
        'LOG_LEVEL': 'ERROR',
        'LOG_LEVEL': 'DUBUG',

    }

    def parse(self, response):

        get_info = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]').css('tr')
        url1="https://nl.wikipedia.org"
        for i in get_info:
            u=i.css('a::attr(href)').getall()
            u="".join(u)
            url =url1+u
            yield scrapy.Request(url,callback=self.detay)
        

    def detay(self,response):
        popu = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody')
        city= response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/caption/b').css(' ::text').get()
        for i in popu:
            tr = i.css('tr')
            for j in tr:
                p = j.css("td ::text").getall()
                # print(p)
                if "Inwoners" in p:
                    p1=p[3]
                    try:
                        population = p1.replace(".","")
                    except:
                        population =p1
                        continue

                elif "Inwoners " in p:
                    p1=p[2]
                    try:
                        population = p1.replace(".","")
                    except:
                        population =p1
                        continue
                elif "Provincie" in p:
                    prvnc=p[1]
            # yield {"city_name":city,"province":prvnc,"population":population}

            if city:
                insert = """ INSERT INTO countries (country_name,city_name,province_name,population) VALUES (%s,%s,%s,%s)"""
                value = ('Netherlands',city,prvnc,population)
                cur.execute(insert, value)
                conn.commit()
