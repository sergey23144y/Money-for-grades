import scrapy
from scrapy.http import HtmlResponse

from items import HtmlacademyParserItem


class HtmlacademySpider(scrapy.Spider):
    name = 'htmlacademy'
    allowed_domains = ['htmlacademy.ru']
    start_urls = ['http://htmlacademy.ru/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//ul[@class='main-nav__list main-nav__list--main']/li[position()>=2]//a/@href").getall()
        for link in links:
            if link != 'https://htmlacademy.ru/intensive':
                yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response: HtmlResponse):
        parse_name = response.xpath("//title/text()").getall()
        parse_price = response.xpath("//span[@data-price='price']//text()").get()
        parse_data = {'parse_name': parse_name, 'parse_price': parse_price}
        if parse_data['parse_price'] is None:
            parse_data['parse_price'] = response.xpath("//div[@class='div-prices-course']//text()").get()
            if parse_data['parse_price'] is None:
                return response.follow(
                    'https://htmlacademy.ru/courses/pro/ultimate-cascade?_ga=2.243910658.642713361.1648139798-2064830407.1647971674',
                    callback=self.parse_cascade, cb_kwargs=dict(parse_dict=parse_data))
            else:
                return HtmlacademyParserItem(htmlacademy_name=parse_data['parse_name'], htmlacademy_price=parse_data['parse_price'])
        else:
            return HtmlacademyParserItem(htmlacademy_name=parse_data['parse_name'], htmlacademy_price=parse_data['parse_price'])

    def parse_cascade(self, response: HtmlResponse, parse_dict):
        parse_dict['parse_price'] = response.xpath("//span[@class='prices__sum']/text()").get()
        return HtmlacademyParserItem(htmlacademy_name=parse_dict['parse_name'], htmlacademy_price=parse_dict['parse_price'])

