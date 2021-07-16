from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruamerlenparser.spiders.leroymerlin_ru import LeroymerlinRuSpider
from leruamerlenparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # input = ('')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinRuSpider, search='губка')

    process.start()