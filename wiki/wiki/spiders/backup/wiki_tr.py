import scrapy
from urllib.parse import quote
import string


class WikiTrSpider(scrapy.Spider):
    name = 'wiki_tr'
    # allowed_domains = ['https://tr.wikipedia.org/wiki/T%C3%BCrkiye'deki_illerin_n%C3%BCfuslar%C4%B1_(2020)']
    # new_url='https://tr.wikipedia.org/wiki/T%25C3%25BCrkiye%27deki_illerin_n%25C3%25BCfuslar%25C4%25B1_%282020%29'

    # url10 = quote(new_url, safe=string.printable)
    start_urls = ["https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_illerin_n%C3%BCfuslar%C4%B1_(2020)"]
    

    def parse(self, response):
        city = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]').css('tr')
        
        print("++++++++++++++++++++++++++++++++++")

        for i in city:   
            city_name =i.xpath('./td[1]/a/text()').extract()
            province1=i.xpath('./td[3]/a/text()').getall()
            province2=i.xpath('./td[3]/text()').getall()
            population=i.xpath('./td[2]/text()').getall()
            city_name = "".join(city_name)
            province1="".join(province1)
            province2="".join(province2)
            population="".join(population)
            # print(city_name)
            if province1:
                p1=province1
            else:
                p1=province2
            yield {"city_name":city_name,"province":p1,"population":population}
            # print(population)
            # print("+++++++++++++++++++++++++++++++")