import scrapy
from scrapy.http import HtmlResponse

from items import RshuParserItem


class RshuSpider(scrapy.Spider):
    name = 'rshu'
    allowed_domains = ['uprav.ru']
    start_urls = ['https://uprav.ru/catalog/?format=DJMGuC3Y',
                  'https://uprav.ru/catalog/?format=DSO',
                  'https://uprav.ru/catalog/?format=HgB3C2NF']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='catalog-courses-item rel col-100-xs']//@href").getall()
        next_page = response.xpath("//li[@class='pagination__item pagination__item--next']//@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_course)

    def parse_course(self, response: HtmlResponse):
        parse_type_of_learning = response.xpath("//a[@class='tab-links__item is-active']/text()").getall()
        parse_name = response.xpath("//div[@class='t-h2']/text()").get()
        parse_training_time = response.xpath("//div[@class='course-info__title']/text()").getall()
        parse_description = response.xpath("//section[4]//div[@class='section__content']//text()").getall()
        parse_course_program = response.xpath("//p[@class='program-item__title']//text()").getall()
        parse_teachers = response.xpath("//div[@class='course-teacher__name']/text()").getall()
        parse_price = response.xpath("//div[@class='order__price-old']/text()").get()
        parse_category = response.xpath("//div[@class='course-info__title']/text()").get()
        yield RshuParserItem(type_of_learning=parse_type_of_learning, name=parse_name, training_time=parse_training_time, description=parse_description,
                               course_program=parse_course_program, teachers=parse_teachers, price=parse_price,
                               category=parse_category)
