import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin

from jobparser.items import JobparserItem

class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']
    loc_domain = 'http://superjob.ru/'

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[contains(@class,'f-test-search-result-item')]//div[contains(@class,'jNMYr')]//a/@href").extract()
        next_page = response.xpath("//a[@rel='next'][position()=2]/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//h1/parent::div/span/span/span/text()').extract()
        link = response.url
        vacancy_company_link = urljoin(self.loc_domain,
                                       response.xpath('//h2/parent::a/@href').extract_first())
        item = JobparserItem(vacancy_name=vacancy_name, salary=salary, link=link,
                             vacancy_company_link=vacancy_company_link)
        yield item
