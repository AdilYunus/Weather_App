from tkinter.tix import PopupMenu
from unittest import result
import scrapy
import re

class WikiUsSpider(scrapy.Spider):
    name = 'wiki_us'
    # allowed_domains = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    custom_setting = {
        'LOG_LEVEL': 'ERROR',
    }

    
    # def parse(self, response):
    #     city_name = response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]').css('tr')
    #     count=0
    #     dict={}
    #     print("#############################################")
    #     for i in city_name:
    #         city = i.css('td ::text').get()
    #         province = i.xpath('./td[2]/a/text()').get()
    #         population = i.xpath('./td[3]/text()').get()
    #         count+=1
    #         print("+++++++++++++++++++++++++++++++++++++")

    #         print(count)
    #         print(city)
    #         print(province)
    #         print(population)
            
    #         # if city_name:
    #         #     dict["city_name"].append(city)
    #         #     dict["province"].append(province)
    #         # print("+++++++++++++++++++++++++++++++++++++")
    #     print(dict)
    #         # yield {"city_name":city,"province":province,"population":population}


    def parse(self, response):
        city_name = response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]').css('tr')
        count=0
        dict={}
        # print("#############################################")
        for i in city_name:
            count+=1
            print(count)
            city = i.css('td ::text').get()
            province = i.xpath('./td[2]/a/text()').get()
            population = i.xpath('./td[3]/text()').get()
            yield {"city_name":city,"province":province,"population":population}
            # print("+++++++++++++++++++++++++++++++++++++")

            # print(count)
            # print(city)
            # print(province)
            # print(population)
            
            # if city_name:
            #     dict["city_name"].append(city)
            #     dict["province"].append(province)
            # print("+++++++++++++++++++++++++++++++++++++")
            # yield {"city_name":city,"province":province,"population":population}
