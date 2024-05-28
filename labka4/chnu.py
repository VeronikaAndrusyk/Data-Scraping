import scrapy


class ChnuSpider(scrapy.Spider):
    name = "chnu"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://chnu.edu.ua"]

    def parse(self, response):
        pass
