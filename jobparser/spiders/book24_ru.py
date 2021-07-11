import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserBookItem


class Book24RuSpider(scrapy.Spider):
    name = 'book24_ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=python']

    def parse(self, response: HtmlResponse):
        books_links = response.xpath(
            "//div[contains(@class,'product-list__item')]//a[contains(@class,'product-card__name smartLink')]/@href").extract()
        next_page = response.xpath("//a[@class='pagination__item _link _button _next smartLink']/@href").extract_first()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_name = response.xpath('//h1/text()').extract_first()
        link = response.url
        author = response.xpath(
            '//ul[@class="product-characteristic__list"]/li[position()=1]//div[@class="product-characteristic__value"]/a/text()').extract_first()
        main_salary = response.xpath("//span[contains(@class,'product-sidebar-price__price-old')]/text()").extract_first()
        sale_salary = response.xpath("//span[contains(@class,'product-sidebar-price__price')]/meta[contains(@itemprop,'price')]/@content").extract_first()
        if not main_salary:
            main_salary = sale_salary
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").extract_first()

        item = JobparserBookItem(book_name=book_name, link=link, author=author,
                                 main_salary=main_salary, sale_salary=sale_salary, rating=rating)
        yield item
