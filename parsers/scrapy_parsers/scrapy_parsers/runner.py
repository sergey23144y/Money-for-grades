from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor

import settings
from spiders.htmlacademy import HtmlacademySpider
from spiders.rshu import RshuSpider


print('running')
crawler_settings = Settings()
crawler_settings.setmodule(settings)
runner = CrawlerRunner(settings=crawler_settings)
runner.crawl(RshuSpider)
runner.crawl(HtmlacademySpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
