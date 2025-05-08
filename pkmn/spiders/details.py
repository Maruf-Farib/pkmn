import scrapy
import json

with open('card_links.json', mode='r', encoding='utf-8') as links_file:
    urls = json.load(links_file)

class DetailsSpider(scrapy.Spider):
    name = "details"
    def start_requests(self):
        sets = urls
        for card_list in sets[:1]:
            setName = card_list['Set Name']
            card_links = card_list['Cards']
            for card in card_links:
                yield scrapy.Request(url=card, callback=self.parse, meta={'Set': setName})

    def parse(self, response):
        card_url = response.url
        image_url = response.xpath("//a[contains(@title, 'Download Image')]/@href").get()
        image_jpg = response.xpath("//a[@class='card-image-link']/@href").get()
        div = response.xpath("//div[@class='card-tabs']")
        type = div.xpath(".//div[@class='type-evolves-is']//a[contains(@href, 'type')]/@href").get()
        name = div.xpath(".//div[@class='name-hp-color']//a[contains(@href, '/name/')]/text()").get().strip()
        serial = div.xpath(".//span[@class='number']//a/text()").get()
        set = response.meta['Set']
        set_link = div.xpath(".//a[contains(@href,'set')]/@href").get() 
        date = div.xpath(".//span[@class='date']/text()").get()[2:]
        rarity = div.xpath(".//a[contains(@href,'rarity')]").xpath("string(.)").get()
        rarity_link = div.xpath(".//a[contains(@href,'rarity')]/@href").get()
        if type != "https://pkmncards.com/type/pokemon/":
            yield {       
                'url': card_url,      
                'ImageJPG': image_jpg,
                'image': image_url,
                'details': {
                    'Name': name,
                    'image': image_url,
                    'type': 'Trainer',
                    'Set': set,
                    'Set Link': set_link,
                    'serial': serial,
                    'Date': date,
                    'Rarity': rarity,
                    'Rarity Link': rarity_link,                                           
                }
            }
            return
        hp = div.xpath(".//a[contains(@href, 'hp')]/text()").get()
        color = div.xpath(".//div[@class='name-hp-color']//abbr/@title").get().strip()
        color_link = div.xpath(".//div[@class='name-hp-color']//a[contains(@href, 'color')]/@href").get()
        pokemon = div.xpath(".//div[@class='type-evolves-is']//a[contains(@href, 'com/pokemon')]/text()").get().strip()
        pokemon_link = div.xpath(".//div[@class='type-evolves-is']//a[contains(@href, 'com/pokemon')]/@href").get()
        stage = div.xpath(".//div[@class='type-evolves-is']//a[contains(@href, 'com/stage')]/text()").get()
        stage_link = div.xpath(".//div[@class='type-evolves-is']//a[contains(@href, 'com/stage')]/@href").get()
        evolves = div.xpath(".//div[@class='type-evolves-is']//span[@class='evolves']//a").xpath("string(.)").getall()
        level = div.xpath(".//a[contains(@href, 'level/')]/text()").get()
        level_link = div.xpath(".//a[contains(@href, 'level/')]/@href").get()
        if(not level):
            level = 'NONE'
            level_link = 'NONE'        
        yield {            
            'url': card_url,
            'ImageJPG': image_jpg,
            'image': image_url,         
            'details': {
                'serial': serial,
                'Name': name,
                'type': 'Pokemon',
                'image': image_url,
                'Pokemon': pokemon,
                'Pokemon Link': pokemon_link,
                'Set': set,
                'Set Link': set_link,
                'Color': color,
                'Color Link': color_link,
                'Stage': stage,
                'Stage Link': stage_link,
                'Rarity': rarity,
                'Rarity Link': rarity_link,
                'Evolution': evolves,
                'Date': date,
                'Level': level,
                'Level Link': level_link,
                'HP': hp,                
            }           
        }