import time
import requests
import pymongo
from lxml.html import fromstring, HtmlElement
from datetime import datetime
from string import whitespace

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class LentaParse:
    date_str_ru = {
        'января': '01',
        'февраля': '02',
        'марата': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }

    def __init__(self, start_url, mongo_url):
        self.start_url = start_url
        client = pymongo.MongoClient(mongo_url)
        self.db = client["newsdb"]
        self.header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

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

    @property
    def template(self):
        data_template = {
            "source": lambda a: "lenta.ru",
            "news_name": lambda a: self.clear_string(a.xpath("./a/text()")[0]),
            "news_url": lambda a: a.xpath("./a/@href")[0],
            "news_date": lambda a: self.date_format(a.xpath("./a/time/@datetime")[0]),
        }
        return data_template

    def run(self):
        for news in self._parse(self.get_xpath(self.start_url)):
            print(news)
            self.save(news)

    def _parse(self, xpath_html):
        news_xpath = xpath_html.xpath(
            "//section[contains(@class,'js-top-seven')]/div[contains(@class,'span4')][position()=2]/div[contains(@class,'item')]"
        )
        for news_tag in news_xpath:
            news_data = {}
            for key, func in self.template.items():
                try:
                    news_data[key] = func(news_tag)
                except AttributeError:
                    pass
            yield news_data

    def save(self, data):
        collection = self.db["magnit"]
        collection.insert_one(data)

    def date_format(self, date):
        date_list = date.split(',')
        news_time = date_list[0].strip()
        news_date = date_list[1].strip()
        news_date_list = news_date.split()
        day = news_date_list[0]
        try:
            month = self.date_str_ru[news_date_list[1]]
        except Exception:
            return None
        year = news_date_list[2]

        date_time_str = f'{year}-{month}-{day} {news_time}'
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

        return date_time_obj

    def clear_string(self, s, whitespaces=CUSTOM_WHITESPACE):
        for space in whitespaces:
            s = s.replace(space, " ")
        return s


if __name__ == "__main__":
    url = "https://lenta.ru/"
    mongo_url = "mongodb://localhost:27017"
    parser = LentaParse(url, mongo_url)
    parser.run()
