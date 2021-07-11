from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hh_uz import HhUzSpider
from jobparser.spiders.superjob_ru import SuperjobRuSpider
from jobparser.spiders.labirint_ru import LabirintRuSpider
from jobparser.spiders.book24_ru import Book24RuSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhUzSpider)
    process.crawl(SuperjobRuSpider)
    process.crawl(LabirintRuSpider)
    process.crawl(Book24RuSpider)

    process.start()
