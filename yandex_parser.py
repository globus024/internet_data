# Azamat Khankhodjaev
# 04.07.2021

from datetime import datetime
from string import whitespace
from abstarct_parser import AbsParser

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class YandexParse(AbsParser):

    def __init__(self, start_url):
        super().__init__(start_url)
        self.start_url = start_url

        self.header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self._data_result = []

    @property
    def template(self):
        data_template = {
            "source": lambda a: a.xpath("./article//a[contains(@class, 'mg-card__source-link')]/@href")[0],
            "news_name": lambda a: self.clear_string(a.xpath("./article//a[contains(@class,'mg-card__link')]/h2/text()")[0]),
            "news_url": lambda a: a.xpath("./article//a[contains(@class,'mg-card__link')]/@href")[0],
            "news_date": lambda a: self.date_format(a.xpath("./article//span[contains(@class, 'mg-card-source__time')]/text()")[0]),
        }
        return data_template

    def _parse(self, xpath_html):
        news_xpath = xpath_html.xpath(
            "//div[contains(@class,'news-app__top')][position()=1]//div[contains(@class, 'mg-grid__col')]"
        )
        for news_tag in news_xpath:
            news_data = {}
            for key, func in self.template.items():
                try:
                    news_data[key] = func(news_tag)
                except AttributeError:
                    pass
            yield news_data


    def date_format(self, date):
        news_time = date
        news_date = datetime.now().strftime('%Y-%m-%d')
        date_time_str =f'{news_date} {news_time}'
        return date_time_str



if __name__ == "__main__":
    url = "https://yandex.ru/news/"

    parser = YandexParse(url)
    parser.run()
