import scrapy
from scrapy.http import HtmlResponse
from leruamerlenparser.items import LeruamerlenparserItem
from scrapy.loader import ItemLoader

class LeroymerlinRuSpider(scrapy.Spider):
    name = 'leroymerlin_ru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinRuSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response):
        goods_links = response.xpath("//a[contains(@data-qa,'product-name')]")
        next_page = response.xpath("//a[contains(@data-qa-pagination-item,'right')]")

        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=LeruamerlenparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@class='ProductHeader__price-default_current-price ']/text()")
        loader.add_xpath('photos', "//img[@class=' PreviewListSmall__image Image']/@src")
        yield loader.load_item()