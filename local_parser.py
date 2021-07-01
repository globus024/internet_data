import bs4
import requests
from pathlib import Path
import json
from abc import ABC, abstractmethod


class ParserAbs(ABC):
    def __init__(self, start_url, parameter, dir_name, file_name):
        self.start_url = start_url
        self.parameter = parameter
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"}
        self._data_result = []
        self.dir_name = dir_name
        self.file_name = file_name

    def get_response(self, url, *args, **kwargs):

        response = requests.get(url, *args, **kwargs)
        if response.status_code == 200:
            return response

        raise ValueError("URL DIE")

    def get_soup(self, url, *args, **kwargs) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(self.get_response(url, *args, **kwargs).text, "html.parser")
        return soup

    @abstractmethod
    def template(self):
        pass

    @abstractmethod
    def format_salary(self, salary):
        pass

    def run(self):
        for job in self._parse(self.get_soup(self.start_url, self.parameter, headers=self.headers)):
            try:
                if job:
                    self._data_result.append(job)
            except KeyError as e:
                print(e)

    @abstractmethod
    def _parse(self, soup):
       pass

    def save(self, data):
        try:
            result_path = self._get_path(self.dir_name)
            file_path = result_path.joinpath(f'{self.file_name}')
            file_path.write_text(json.dumps(data))
        except Exception as ex:
            print("saved", ex)

    def _get_path(self, dir_name):
        file_path = Path(__file__).parent.joinpath(dir_name)
        if not file_path.exists():
            file_path.mkdir()
        return file_path

    def get_data(self):
        return self._data_result
