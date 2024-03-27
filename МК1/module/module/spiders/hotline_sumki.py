import scrapy

class HotlineSumkiSpider(scrapy.Spider):
    name = 'hotline_sumki'
    start_urls = ['https://hotline.ua/ua/fashion/sumki/']

    def parse(self, response):
        for product in response.css('div.catalog.container div.list-item'):
            title = product.css('a.item-title::text').get().strip()
            link = response.urljoin(product.css('a.item-title::attr(href)').get())
            image = response.urljoin(product.css('div.list-item__photo img::attr(src)').get())
            price = product.css('div.list-item__value-price::text').get().strip()
            offers = product.css('a::text').re_first(r'(\d+) пропозицій?')

            # Переходимо на сторінку кожного товару для отримання інформації про магазини
            yield scrapy.Request(url=link, callback=self.parse_product_details, meta={'title': title, 'link': link, 'image': image, 'price': price, 'offers': offers})

    def parse_product_details(self, response):
        title = response.meta['title']
        link = response.meta['link']
        image = response.meta['image']
        price = response.meta['price']
        offers = response.meta['offers']

        # Парсимо назву магазину
        shop_name = response.css('a.shop__title::text').get().strip()

        yield {
            'title': title,
            'link': link,
            'image': image,
            'price': price,
            'offers': offers,
            'shop_name': shop_name
        }
