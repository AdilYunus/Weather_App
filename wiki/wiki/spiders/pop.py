import scrapy


class PopSpider(scrapy.Spider):
    name = 'pop'
    # allowed_domains = ['https://nl.wikipedia.org/wiki/Aardenburg_(stad)']
    start_urls = ['http://https://nl.wikipedia.org/wiki/Aardenburg_%28stad%29']

    def parse(self, response):
        get_pop = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]')

        # //*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[9]/td[1]/a
        for i in get_pop:
            print("************************************")
            pop2=i.xpath('./tr/td/a[contains(text(),"Inwoners")]').getall()
            # pop1=i.xpath('./tr[text()="Inwoners"]/following-sibling::td//text()').getall()
            print(pop2)
            print("************************************")


