import json
import logging

from src.abc_fileio import FileManager
from src.models import Vacancy


class VacanciesManager(FileManager):
    path: str | None
    vacancies: list[Vacancy]

    def __init__(self, path: str | None = None):
        if path:
            if not isinstance(path, str):
                raise TypeError("A string expected for the file path")
            with open(path) as file:
                vacs = json.load(file)
            if (
                not isinstance(vacs, dict)
                or "items" not in vacs.keys()
                or not isinstance(vacs["items"], list)
            ):
                logging.warning(f"Bad file {path}")
                self.vacancies = []
            else:
                self.vacancies = [Vacancy.from_dict(v) for v in vacs["items"]]
        else:
            self.vacancies = []
        self.path = path

    def add(self, item):
        if isinstance(item, Vacancy):
            self.vacancies.append(item)
        else:
            raise TypeError("A vacancy object expected to add")

    def remove(self, n: int):
        if not isinstance(n, int):
            raise TypeError("A number of vacancy expected for removing")
        if n < 0 or n >= len(self.vacancies):
            raise IndexError("Vacancy index out of range")
        self.vacancies.pop(n)

    def sort(self, reverse: bool = True):
        if not isinstance(reverse, bool):
            raise TypeError("A bool expected for reverse flag")
        self.vacancies.sort(reverse=reverse)

    def filter(self):
        self.vacancies = [v for v in self.vacancies if v.salary_to or v.salary_from]

    def save(self, path: str | None = None):
        if path:
            if not isinstance(path, str):
                raise TypeError("A string expected for the file path")
        else:
            path = self.path
        with open(path, "w") as file:
            json.dump({"items": [v.to_dict() for v in self.vacancies]}, file)
        self.path = path

    def clear(self):
        self.vacancies = []
