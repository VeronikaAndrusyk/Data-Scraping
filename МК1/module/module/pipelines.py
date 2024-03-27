import scrapy
from scrapy.exceptions import DropItem

class OfferFilterPipeline:
    def process_item(self, item, spider):
        # Якщо кількість пропозицій менше 10, видаляємо товар з результатів
        if item['offers'] is not None and int(item['offers']) < 10:
            raise DropItem(f"Товар '{item['title']}' має менше 10 пропозицій")
        else:
            return item
