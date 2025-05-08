import scrapy
import json

#with open('links.json', mode='r', encoding='utf-8') as links_file:
#    urls = json.load(links_file)  

class CardsSpider(scrapy.Spider):
    name = "cards"
    
    def start_requests(self):
        #links = urls
        links = ["https://pkmncards.com/set/stellar-crown/"]
        for link in links:
            name = 'Stellar Crown'
            yield scrapy.Request(url=link, callback=self.parse, meta={'setName': name})

    def parse(self, response):
        setName = response.meta['setName']
        card_list = []
        card_urls = response.xpath("//a[@class='card-image-link']")
        for url in card_urls:            
            url = url.xpath(".//@href").get()
            card_list.append(url)
        yield {
            'Set Name': setName,
            'Cards': card_list
        }
