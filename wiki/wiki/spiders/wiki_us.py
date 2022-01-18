from unittest import result
import scrapy
import re
import psycopg2

conn = psycopg2.connect(database="Weather_App",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
cur = conn.cursor()

class WikiUsSpider(scrapy.Spider):
    name = 'wiki_us'
    # allowed_domains = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    custom_setting = {
        'LOG_LEVEL': 'ERROR',
    }

    def parse(self, response):
        getinfo = response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]').css('tr')
        count=0
        for i in getinfo:
            count+=1
            city = i.css('td ::text').get()
            province = i.xpath('./td[2]/a/text()').get()
            population = i.xpath('./td[3]/text()').extract()
            population="".join(population)
            pop=population.replace(",","")
            pop1=(pop.replace("\n",""))
            pop2 =pop1.strip()
            # yield {"city_name":city,"province":province,"population":pop2}
            #------------insert database

            if city is not None:
                insert = """ INSERT INTO countries (country_name,city_name,province_name,population) VALUES (%s,%s,%s,%s)"""
                value = ('USA', city,province,pop2)
                cur.execute(insert, value)

        conn.commit()
        conn.close()

