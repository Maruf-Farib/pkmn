import scrapy
import json

with open('card_links.json', mode='r', encoding='utf-8') as links_file:
    urls = json.load(links_file)
    
unique = []
class UniqueSpider(scrapy.Spider):
    name = "unique"
    def start_requests(self):
        sets = urls
        for card_list in sets:
            card_links = card_list['Cards']
            for card in card_links:
                yield scrapy.Request(url=card, callback=self.parse)

    def parse(self, response):
        a = response.xpath("//span[@class='pokemon']/a")
        if len(a)>0:
            name = a.xpath(".//text()").get()
            name = name.strip()
            url = a.xpath(".//@href").get()
            if url not in unique:
                unique.append(url)
                yield {
                    'Name': name,
                    'Link': url
                }
