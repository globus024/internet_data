import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
from jobparser.items import JobparserBookItem


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']
    loc_domain = 'https://www.labirint.ru/'

    def parse(self, response: HtmlResponse):
        books_links = response.xpath(
            "//div[contains(@class,'card-column')]//a[contains(@class,'product-title-link')]/@href").extract()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_name = response.xpath('//h1/text()').extract_first()
        link = response.url
        author = response.xpath('//div[@class="authors"]/a/text()').extract()
        main_salary = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        sale_salary = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='product-rating-marks-label']/text()").extract_first()

        item = JobparserBookItem(book_name=book_name, link=link, author=author,
                                 main_salary=main_salary, sale_salary=sale_salary, rating=rating)
        yield item
