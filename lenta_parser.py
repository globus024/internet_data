# Azamat Khankhodjaev
# 04.07.2021

from datetime import datetime
from string import whitespace
from abstarct_parser import AbsParser
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class LentaParse(AbsParser):
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
            "source": lambda a: "lenta.ru",
            "news_name": lambda a: self.clear_string(a.xpath("./a/text()")[0]),
            "news_url": lambda a: a.xpath("./a/@href")[0],
            "news_date": lambda a: self.date_format(a.xpath("./a/time/@datetime")[0]),
        }
        return data_template


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
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M')

        return date_time_obj




if __name__ == "__main__":
    url = "https://lenta.ru/"
    parser = LentaParse(url)
    parser.run()
