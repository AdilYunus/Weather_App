from cgi import print_environ_usage
from distutils.log import info
from itertools import count
from types import CoroutineType
from typing import Counter, Text
from urllib.parse import urlunparse
import scrapy
import time


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
        self.count =0
        for i in get_info:
            # print("************************************")
            u=i.css('a::attr(href)').getall()
            u="".join(u)
            url =url1+u
            yield scrapy.Request(url,callback=self.detay)
            # print("-------------------------------")
    # def parse(self, response):
    #     pop = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr/td/a@href').extract
    #     for i in pop:
    #         url=response.urljoin(i)
    #         yield scrapy.Request(url,callback=self.detay)
    def detay(self,response):
        # time.sleep(1)
        self.count+=1
        # print("+++++++++++++++++++++++++++++++++++")
        popu = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody')
        city= response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/caption/b').css(' ::text').get()
        # city =response.xpath('')
        for i in popu:
            tr = i.css('tr')
            for j in tr:
                p = j.css("td ::text").getall()
                # print(p)
                if "Inwoners" in p:
                    p1=p[3]
                elif "Inwoners " in p:
                    p1=p[2]
                elif "Provincie" in p:
                    prvnc=p[1]
            yield {"city_name":city,"province":prvnc,"population":p1}
        # print(po2)
        # print("-------------------------------")
    
#     def detail(self, response):
#         info =response.xpath(''//*[@id="mw-content-text"]/div[1]/table[1]/tbody')
#         for i in info:
#             tr = i.css('tr')
#             for j in tr:
#                 p = j.css("td ::text").getall()
#                 if "Inwoners" in p:
#                     print(p[3])
#                 elif "Inwoners " in p:
#                     print(p[2]) """
            





#     def detay(self,response):
#         pop =response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]').css('tr')
        
        
#         print("+++++++++++++++++++++++++++++++++++++++++")
#         # //*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[9]/td[2]
#         for p in pop:
#             # pop1=p.xpath('./td[text()="Inwoners "]/following-sibling::td//text()[1]').get()
#             pop2=p.xpath('./td/a[contains(text(),"Inwoners")]/following-sibling::td//text()[1]').getall()

#             # .//th[text()="Item Code"]/following-sibling::td//text()
            
#             # pop1=pop.xpath('./td[2]/text()').get()
#             # if pop1 =="Inwoners":
#             #     print('goooooooooooooooood')
#         # pop1 = pop.css('td ::text').extract()
        
#             print(f'population--{pop2}')
#         print("+++++++++++++++++++++++++++++++++++++++++")


# # class WikiNlSpider(scrapy.Spider):
# #     name = 'wiki_nl'
# #     # allowed_domains = ['nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen_met_stadsrechten']
# #     start_urls = ['https://nl.wikipedia.org/wiki/Lijst_van_Nederlandse_plaatsen_met_stadsrechten']

# #     def parse(self, response):

# #         get_info = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr/td/a@href').extract()
# #         print(get_info)




# #     def detail(self,response):
        
# #         print("***********************************")
# #         popu = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody')
# #         for i in popu:
# #             tr = i.css('tr')
# #             for j in tr:
# #                 p = j.css("td ::text").getall()
# #                 if "Inwoners" in p:
# #                     print(p[3])
# #                 elif "Inwoners " in p:
# #                     print(p[2])
