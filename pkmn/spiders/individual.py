import scrapy
import json
with open('unique.json', mode='r', encoding='utf8') as f:
            database = json.load(f)

class IndividualSpider(scrapy.Spider):
    name = 'individual'

    def start_requests(self):
        data = database
        for entry in data:
            yield scrapy.Request(url=entry['Link'], callback=self.parse, meta={'name': entry['Name'], 'urls': []})

    def parse(self, response):
        links = response.xpath("//div[@class='entry-content']//img/@src").getall()  
        response.meta['urls'].extend(links)

        next_page = response.xpath("//a[contains(text(), 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse, meta=response.meta)
        else:
            yield {
                'name': response.meta['name'],
                'urls': response.meta['urls']
            }


