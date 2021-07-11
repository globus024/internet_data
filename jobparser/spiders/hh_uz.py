import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin

from jobparser.items import JobparserItem


class HhUzSpider(scrapy.Spider):
    name = 'hhuz'
    allowed_domains = ['hh.uz']
    loc_domain = 'https://tashkent.hh.uz'
    start_urls = [
        'https://tashkent.hh.uz/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').extract_first()
        salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract_first()
        link = response.url
        vacancy_company_link = urljoin(self.loc_domain,
                                       response.xpath('//a[@class="vacancy-company-name"]/@href').extract_first())
        item = JobparserItem(vacancy_name=vacancy_name, salary=salary, link=link, vacancy_company_link=vacancy_company_link)
        yield item

