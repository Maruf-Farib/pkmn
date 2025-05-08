import scrapy
import json

with open('card_links.json', mode='r', encoding='utf-8') as links_file:
    urls = json.load(links_file)

class ImagesSpider(scrapy.Spider):
    name = "images"
    def start_requests(self):
        sets = urls
        for card_list in sets[:1]:
            setName = 'Stellar Crown'
            card_links = card_list['Cards']
            total_cards = len(card_links)
            grouped_data = {'setName': setName, 'cards': []}
            for card in card_links:
                yield scrapy.Request(url=card, callback=self.parse, meta={'setName': setName, 'grouped_data': grouped_data, 'total': total_cards})

    def parse(self, response):
        setName = response.meta['setName']
        grouped_data = response.meta['grouped_data']
        total_cards = response.meta['total']
        
        image_url = response.xpath("//a[@class='card-image-link']/@href").get()
        
        grouped_data['cards'].append(image_url)
        
        if len(grouped_data['cards']) == total_cards:
            yield grouped_data
