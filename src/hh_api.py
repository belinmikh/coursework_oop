import logging

import requests

from src.abc_api import BaseAPI


class HH(BaseAPI):
    __url: str
    __headers: dict
    __params: dict

    __slots__ = ("__url", "__headers", "__params")

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def get(self, arg) -> list:
        to_return = []
        self.__params["text"] = arg
        while self.__params.get("page") != 20:
            response_json = requests.get(self.__url, headers=self.__headers, params=self.__params).json()
            try:
                to_return.extend(response_json["items"])
            except KeyError:
                logging.warning(
                    f"hh.ru has no items or broken"
                )
                return to_return
            self.__params["page"] += 1
        self.__params["page"] = 0
        return to_return
