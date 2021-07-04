# Azamat Khankhodjaev
# 04.07.2021

from datetime import datetime
from string import whitespace
from abstarct_parser import AbsParser
from mail_parser_children import MailRuChildrenParse

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class MailRuParse(AbsParser):


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
            "link": lambda a: self.clear_string(a.xpath("./a[contains(@class, 'js-topnews__item')]/@href")[0]),
        }
        return data_template


    def _parse(self, xpath_html):
        news_xpath = xpath_html.xpath(
            "//div[contains(@class,'js-topnews')]//div[contains(@class,'daynews__item')]"
        )
        for news_tag in news_xpath:
            news_data = {}
            for key, func in self.template.items():
                try:
                    news_data[key] = func(news_tag)
                except AttributeError:
                    pass
            yield news_data

    def run(self):
        for news in self._parse(self.get_xpath(self.start_url)):
            self._data_result.append(news)
        if self._data_result:
            for val in self._data_result:
                url = val['link']
                parser = MailRuChildrenParse(url)
                parser.run()

    def date_format(self, date):

       pass




if __name__ == "__main__":
    url = "https://news.mail.ru/"
    parser = MailRuParse(url)
    parser.run()
