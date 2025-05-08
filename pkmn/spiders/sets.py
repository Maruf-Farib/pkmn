import scrapy


class SetsSpider(scrapy.Spider):
    name = "sets"
    allowed_domains = ["https://pkmncards.com"]
    start_urls = ["https://pkmncards.com/sets/"]

    def parse(self, response):
        links = response.xpath("//div[@class='entry-content']//a[contains(@href, '/set/')]")
        for link in links:
            name = link.xpath('.//text()').get()
            link = link.xpath('.//@href').get()
            yield {
                'Name': name,
                'url': link
            }
            
            
