import scrapy

class FacultyItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()


class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    faculty = scrapy.Field()

class StaffItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()

