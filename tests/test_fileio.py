from typing import Any
from unittest.mock import patch

import pytest

from src.fileio import VacanciesManager
from src.models import Vacancy


@patch("builtins.open")
@patch("json.load")
def test_vm_init(load_mock: Any, open_mock: Any, vacs_file: Any) -> None:
    load_mock.return_value = vacs_file

    vm_empty = VacanciesManager()
    assert vm_empty.vacancies == []

    vm_from_file = VacanciesManager('some_file.json')
    expected =  [Vacancy.from_dict(v) for v in vacs_file['items']]
    for v0, v1 in zip(vm_from_file.vacancies, expected):
        assert v0.__dict__ == v1.__dict__

    with pytest.raises(TypeError):
        VacanciesManager(123)


@patch("builtins.open")
@patch("json.load")
def test_vm_kinda_crud(load_mock: Any, open_mock: Any, vacs_file: Any) -> None:
    load_mock.return_value = vacs_file
    vm_from_file = VacanciesManager('some_file.json')

    vm_from_file.sort()
    for i in range(len(vm_from_file.vacancies) - 2):
        assert vm_from_file.vacancies[i].salary_mean >= vm_from_file.vacancies[i + 1].salary_mean

    vm_from_file.filter()
    for v in vm_from_file.vacancies:
        assert v.salary_from or v.salary_to

    with pytest.raises(TypeError):
        vm_from_file.add(123)

    v = Vacancy('abc')
    vm_from_file.add(v)
    assert vm_from_file.vacancies[-1] == v

    prev_len = len(vm_from_file.vacancies)
    vm_from_file.remove(prev_len - 1)
    assert prev_len - len(vm_from_file.vacancies) == 1

    vm_from_file.clear()
    assert vm_from_file.vacancies == []
