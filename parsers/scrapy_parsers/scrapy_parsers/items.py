# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class HtmlacademyParserItem(scrapy.Item):
    htmlacademy_name = scrapy.Field()
    htmlacademy_price = scrapy.Field()


class RshuParserItem(scrapy.Item):
    name = scrapy.Field()
    training_time = scrapy.Field()
    description = scrapy.Field()
    course_program = scrapy.Field()
    teachers = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    type_of_learning = scrapy.Field()