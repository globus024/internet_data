# Khankhodjaev Azamat
# 01.07.2021
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов Superjob(по желанию) и HH(обязательно). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import time
import pandas as pd
from local_parser import ParserAbs
class SuperJobParse(ParserAbs):

    def __init__(self, start_url, parameter, dir_name, file_name):
        super().__init__(start_url, parameter, dir_name, file_name)
        self.start_url = start_url
        self.parameter = parameter
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"}
        self._data_result = []
        self.dir_name = dir_name
        self.file_name = file_name

    @property
    def template(self):
        data_template = {
            "name": lambda a: a.find('a').text,
            "salary": lambda a: self.format_salary(a.find('span', attrs={'class':'_1OuF_ _1qw9T f-test-text-company-item-salary'}).text),
            "vac_link": lambda a: "https://www.superjob.ru"+a.find('a').get('href'),
            "outer_link":lambda a: "https://www.superjob.ru"+a.find('span',
                                                                    attrs={'class':'_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc'}).find('a').get('href'),
        }
        return data_template

    def format_salary(self, salary):
        try:
            salary =str(salary)
            salary = salary.replace("руб./месяц", "").replace("от", "").replace('до', '')
            salary = salary.replace(' ', '').replace('Поговорённости','').replace('—', ' ')
            salary_list = salary.split()
            return float(salary_list[0])
        except Exception:
            return 0.0



    def _parse(self, soup):
        job_a = soup.find_all("div", attrs={"class": "f-test-search-result-item"})
        for job_tag in job_a:
            job_data = {}
            for key, func in self.template.items():
                try:
                    job_data[key] = func(job_tag)
                except AttributeError:
                    pass
            yield job_data


if __name__=="__main__":
    url = "https://www.superjob.ru/vacancy/search"
    parameter ={
        'keywords':'программист',
    }
    parser = SuperJobParse(url, parameter, 'data', 'superjob.json')
    for i in range(1,5):
        parser.parameter['page'] = i
        parser.run()
        time.sleep(1)

    data = parser.get_data()
    parser.save(data)
    df = pd.DataFrame(data, columns =['name', 'salary'])
    print(df)
