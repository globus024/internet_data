# Azamat Khankhodjaev
# 04.07.2021

from datetime import datetime
from string import whitespace
from abstarct_parser import AbsParser

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class MailRuChildrenParse(AbsParser):

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
            "source": lambda a: "news.mail.ru",
            "news_name": lambda a: self.clear_string(a.xpath("//h1[contains(@class,'hdr__inner')]/text()")[0]),
            "news_url": lambda a: self.start_url,
            "news_date": lambda a: self.date_format(a.xpath("//span[contains(@class, 'js-ago')]/@datetime")[0]),
        }
        return data_template

    def _parse(self, xpath_html):
        news_xpath = xpath_html.xpath(
            "//div[contains(@class,'js-module')]"
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
        date_list = date.split('T')
        news_time = date_list[1].strip().split('+')[0]
        news_date = date_list[0].strip()
        date_time_str =f'{news_date} {news_time}'
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
        return date_time_obj



if __name__ == "__main__":
    pass
