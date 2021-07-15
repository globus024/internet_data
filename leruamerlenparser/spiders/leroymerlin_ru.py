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

    def parse(self, response:HtmlResponse):
        goods_links = response.xpath("//a[contains(@data-qa,'product-name')]")
        next_page = response.xpath("//a[contains(@data-qa-pagination-item,'right')]/@href").extract_first()

        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruamerlenparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('article', "//span[@slot='article']/text()")
        loader.add_value('link',response.url)
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src | //img[@slot='thumbs-tail']/@src")

        yield loader.load_item()