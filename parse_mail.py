from selenium.common.exceptions import NoSuchElementException
from string import whitespace
from datetime import datetime, timedelta, date

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


class ParserMail:
    date_str_ru = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
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

    def __init__(self):
        self.uniq = []

    @property
    def template(self):
        data_template = {
            "link": lambda a: a.get_attribute('href'),
            "from": lambda a: a.find_element_by_class_name('ll-crpt').get_attribute('title'),
            "title": lambda a: self.clear_string(a.find_element_by_class_name('ll-sj__normal').text),
            'send_date': lambda a: self.date_format(a.find_element_by_class_name('llc__item_date').get_attribute('title')),
        }
        return data_template

    def parse(self, tags):
        res = []
        for tag in tags:
            data = {}
            for key, func in self.template.items():
                try:
                    data[key] = func(tag)
                except NoSuchElementException:
                    continue
            if data['link'] in self.uniq or 'from' not in data:
                continue
            self.uniq.append(data['link'])
            res.append(data)
        return res

    def clear_string(self, s, whitespaces=CUSTOM_WHITESPACE):
        for space in whitespaces:
            s = s.replace(space, " ")
        return s

    def date_format(self, date_input: str):
        date_list = date_input.split()
        first_part = date_list[0]
        current_year = datetime.now().strftime('%Y')

        if first_part in ["Сегодня,", "Вчера,"]:
            if first_part in "Сегодня,":
                date_str = datetime.now().strftime('%Y-%m-%d')
            else:
                yesterday = date.today() - timedelta(days=1)
                date_str = yesterday.strftime('%Y-%m-%d')

            date_str = f'{date_str} {date_list[1]}'
        else:
            first_part = '{0:0>2}'.format(first_part)
            date_month = self.date_str_ru[date_list[1].lower().replace(',', '')]
            date_year = date_list[2].replace(',', '')
            try:
                date_year = datetime.strptime(date_year, '%Y').strftime('%Y')
                time_str = date_list[3]
            except ValueError:
                time_str = date_year
                date_year = current_year

            date_str = f'{date_year}-{date_month}-{first_part} {time_str}'

        return date_str


if __name__ == '__main__':
    mail_parse = ParserMail()
    a = ['6 января, 7:00', '17 марта 2019, 13:29', 'Сегодня, 13:24', 'Вчера, 21:29']
    for aa in a:
        print(mail_parse.date_format(aa))
