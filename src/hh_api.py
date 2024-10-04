import logging

import requests

from src.abc_api import BaseAPI


class HH(BaseAPI):
    url: str
    headers: dict
    params: dict

    __slots__ = ("url", "headers", "params")

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}

    def get(self, arg) -> list:
        to_return = []
        self.params["text"] = arg
        while self.params.get("page") != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            try:
                to_return.extend(response.json()["items"])
            except KeyError:
                logging.warning(
                    f"hh.ru has no items having status {response.status_code}"
                )
                return to_return
            self.params["page"] += 1
        self.params["page"] = 0
        return to_return


# class HH:
#     """
#     Класс для работы с API HeadHunter
#     Класс Parser является родительским классом, который вам необходимо реализовать
#     """
#
#     def __init__(self):
#         self.url = 'https://api.hh.ru/vacancies'
#         self.headers = {'User-Agent': 'HH-User-Agent'}
#         self.params = {'text': '', 'page': 0, 'per_page': 100}
#         self.vacancies = []
#
#     def load_vacancies(self, keyword):
#         self.params['text'] = keyword
#         while self.params.get('page') != 20:
#             response = requests.get(self.url, headers=self.headers, params=self.params)
#             vacancies = response.json()['items']
#             self.vacancies.extend(vacancies)
#             self.params['page'] += 1
