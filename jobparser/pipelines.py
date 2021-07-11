# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
import pymongo
from string import whitespace
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")

class JobparserPipeline:
    def __init__(self):
        conn_dsn = f'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(conn_dsn)
        self.db = self.client['less6']

    def process_item(self, item, spider):

        if spider.name not in ['hhuz', 'superjob_ru']:
            return item

        loc_dict = dict(item)

        if spider.name == "hhuz":
            loc_dict['salary_min'], loc_dict['salary_max'], loc_dict['currency'] = self.salary_parse_hh(
                loc_dict['salary'])
        elif spider.name == "superjob_ru":
            loc_dict['salary_min'], loc_dict['salary_max'], loc_dict['currency'] = self.salary_parse_superjob(
                loc_dict['salary'])
        del loc_dict['salary']

        self.save(self.db[spider.name], loc_dict)
        return item

    def salary_parse_hh(self, salary_str):
        currency, salary_min, salary_max = None, None, None
        salary = str(salary_str)
        salary = salary.replace('-', '').replace("от", "").replace('до', '-').replace(' ', '').replace('\xa0',
                                                                                                       '').replace(' ',
                                                                                                                   '')
        other_text = re.sub('(\d)', '', salary).replace('-', '')
        if ('руб' in other_text) or ('Руб' in other_text) or ('РУБ' in other_text):
            currency = 'руб'
        elif ('usd' in other_text) or ('USD' in other_text):
            currency = 'usd'
        elif ('eur' in other_text) or ('EUR' in other_text):
            currency = 'eur'

        salary = salary.replace(other_text, '')
        if "-" in salary:
            try:
                salary_min = float(salary.split('-')[0])
            except ValueError:
                salary_min = None
            try:
                salary_max = float(salary.split('-')[1])
            except ValueError:
                salary_max = None
        else:
            try:
                salary_min = float(salary)
            except ValueError:
                salary_min = None

        return salary_min, salary_max, currency

    def salary_parse_superjob(self, salary_list):
        currency, salary_min, salary_max = None, None, None
        salary_str, salary_res = '', []
        for salary in salary_list:
            salary = salary.replace('\xa0', '').replace(' ', '')
            salary = salary.replace('от', '').replace('до', '-')
            if ('руб' in salary) or ('Руб' in salary) or ('РУБ' in salary):
                currency = 'руб'
            elif ('usd' in salary) or ('USD' in salary):
                currency = 'usd'
            elif ('eur' in salary) or ('EUR' in salary):
                currency = 'eur'

            salary = re.sub('\D+', '', salary)
            if salary:
                salary_res.append(salary)

        if len(salary_res) > 1:
            try:
                salary_min = float(salary_res[0])
            except ValueError:
                salary_min = None
            try:
                salary_max = float(salary_res[1])
            except ValueError:
                salary_max = None
        elif len(salary_res) == 1:
            try:
                salary_min = float(salary_res[0])
            except ValueError:
                salary_min = None

        return salary_min, salary_max, currency

    def save(self, collection, data):
        update_data = {}

        filter = {}
        for key in data:
            filter[key] = {'$eq': data[key]}
        update_data['$set'] = data
        collection.update_one(filter, update_data, upsert=True)


class JobparserBookPipeline:
    def __init__(self):
        conn_dsn = f'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(conn_dsn)
        self.db = self.client['less6']

    def process_item(self, item, spider):
        if spider.name not in ['labirint_ru', 'book24_ru']:
            return item

        loc_dict = dict(item)

        if spider.name in "labirint_ru":
            loc_dict['main_salary'], loc_dict['sale_salary'] = self.salary_parse_labirint(loc_dict['main_salary'],
                                                                                          loc_dict['sale_salary'])
        elif spider.name in "book24_ru":
            loc_dict['book_name'] = self.clear_string(loc_dict['book_name'])
            loc_dict['author'] = self.clear_string(loc_dict['author'])
            loc_dict['main_salary'], loc_dict['sale_salary'] = self.salary_parse_book24(loc_dict['main_salary'],
                                                                                        loc_dict['sale_salary'])

        loc_dict['rating'] = self.rating_formats(loc_dict['rating'])

        self.save(self.db[spider.name], loc_dict)
        return item

    def salary_parse_labirint(self, main_salary, sale_salary):
        try:
            main_salary = float(main_salary)
        except ValueError:
            main_salary = None
        except TypeError:
            main_salary = None

        try:
            sale_salary = float(sale_salary)
        except ValueError:
            sale_salary = None
        except TypeError:
            sale_salary = None
        return main_salary, sale_salary

    def salary_parse_book24(self, main_salary, sale_salary):
        if main_salary:
            main_salary = re.sub('\D+', '', main_salary)
            main_salary = main_salary.replace("₽", "").replace(" ", "")
        if sale_salary:
            sale_salary = re.sub('\D+', '', sale_salary)
            sale_salary = sale_salary.replace("₽", "").replace(" ", "")

        try:
            main_salary = float(main_salary)
        except ValueError:
            main_salary = None
        except TypeError:
            main_salary = None

        try:
            sale_salary = float(sale_salary)
        except ValueError:
            sale_salary = None
        except TypeError:
            sale_salary = None
        return main_salary, sale_salary

    def rating_formats(self, rating):
        rating = self.clear_string(re.sub('\D+', '', rating))
        if not rating:
            rating = 0
        try:
            rating = float(rating)
        except ValueError:
            rating = 0

        return rating

    def clear_string(self, s, whitespaces=CUSTOM_WHITESPACE):
        for space in whitespaces:
            s = s.replace(space, " ")
        return s

    def save(self, collection, data):
        update_data = {}

        filter = {}
        filter['link'] = {'$eq': data['link']}
        update_data['$set'] = data
        collection.update_one(filter, update_data, upsert=True)
