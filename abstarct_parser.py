# Azamat Khankhodjaev
# 04.07.2021

import time
import requests
from lxml.html import fromstring, HtmlElement
from string import whitespace
from news_model import NewsModel
from abc import ABC, abstractmethod
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class AbsParser(ABC):


    def __init__(self, start_url):
        self.start_url = start_url
        self.header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.news_model = NewsModel('news_database', 'news')
        self._data_result = []

    def get_response(self, url, *args, **kwargs):
        for _ in range(5):
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(1)
        raise ValueError("URL DIE")

    def get_xpath(self, url, *args, **kwargs) -> HtmlElement:
        dom = fromstring(self.get_response(url, headers=self.header, **kwargs).text)
        return dom

    @abstractmethod
    def template(self):
       pass

    def run(self):
        for news in self._parse(self.get_xpath(self.start_url)):
            self.save(news)

    @abstractmethod
    def _parse(self, xpath_html):
       pass

    def save(self, data):
        self.news_model.save(data)


    @abstractmethod
    def date_format(self, date):
       pass

    def clear_string(self, s, whitespaces=CUSTOM_WHITESPACE):
        for space in whitespaces:
            s = s.replace(space, " ")
        return s


if __name__ == "__main__":
    pass
