# Azamat Khankhodjaev
# 29.06.2021
# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import env
import requests
from pprint import pprint
from typing import Dict, List
from pathlib import Path
import json


# USERNAME: globus024
class GitHubParse:
    def __init__(self, url:str, headers:Dict, dir_name, file_name):
        self.url = url
        self.headers = headers
        self.dir_name = dir_name
        self.file_name = file_name
        self.abs_path = f'{dir_name}/{file_name}'

    def _get_response(self,url, *args, **kwargs):
        response = requests.get(url, *args, **kwargs)
        if response.status_code == 200:
            return response.json()
        raise ValueError("URL DIE")


    def _parse(self, response: Dict) -> List:
        res = []
        for r in response:
            res.append({'url': r['html_url'], 'created_at': r['created_at']})
        return res


    def _save(self):
        response = self._get_response(self.url, self.headers)
        data = self._parse(response)
        result_path = self._get_path(self.dir_name)
        file_path = result_path.joinpath(f'{file_name}')
        file_path.write_text(json.dumps(data))


    def _read_data(self, abs_path: str):
        with open(abs_path,encoding='utf-8') as json_file:
            return json.load(json_file)

    def _get_path(self, dir_name):
        file_path = Path(__file__).parent.joinpath(dir_name)
        if not file_path.exists():
            file_path.mkdir()
        return file_path


    def get_repositories(self):
        try:
            r_json = self._read_data(self.abs_path)
            return [r['url'] for r in r_json if r['url']]
        except KeyError as k:
            return []


    def run(self):
        self._save()

if __name__ == '__main__':

    url = f"https://api.github.com/users/{env.USERNAME}/repos"
    headers = {
        "Authorization":''
    }

    dir_name = "data"
    file_name = 'repos.json'
    github_parse = GitHubParse(url, headers, dir_name, file_name)
    github_parse.run()
    pprint(github_parse.get_repositories())


