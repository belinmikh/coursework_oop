from typing import Any

import pytest

from src.models import Vacancy


@pytest.mark.parametrize(
    "name, requirement, url, salary_from, salary_to, salary_currency",
    [
        (123, "req0", "url0", 123, 456, "RUR"),
        ("name1", 123, "url1", 123, 456, "RUR"),
        ("name2", "req2", 123, 123, 456, "RUR"),
        ("name3", "req3", "url3", "abc", 456, "RUR"),
        ("name4", "req4", "url4", 123, "abc", "RUR"),
        ("name5", "req5", "url5", 123, 456, 123)
    ]
)
def test_vacancy_init_raises(
        name: Any,
        requirement: Any,
        url: Any,
        salary_from: Any,
        salary_to: Any,
        salary_currency: Any
) -> None:
    with pytest.raises(TypeError):
        Vacancy(name, requirement, url, salary_from, salary_to, salary_currency)


def test_vacancy_init() -> None:
    v = Vacancy(
        "name0", "req0", "url0",
        100, 200, "RUR"
    )

    assert v.name == "name0"
    assert v.requirement == "req0"
    assert v.url == "url0"

    assert v.salary_from == 100
    assert v.salary_to == 200

    assert v.salary_mean == 150

    assert v.salary_currency == "RUR"


def test_vacancy_comparing() -> None:
    v0 = Vacancy("v0", salary_from=100)
    v1 = Vacancy("v1", salary_from=100, salary_to=200)
    v2 = Vacancy("v2", salary_to=200)

    assert v0 < v1
    assert v1 < v2
    assert v0 < v2


def test_vacancy_to_dict() -> None:
    assert Vacancy(
        "name0", "req0", "url0",
        100, 200, "RUR"
    ).to_dict() == {
        "name": "name0",
        "snippet": {"requirement": "req0"},
        "alternate_url": "url0",
        "salary": {
            "from": 100,
            "to": 200,
            "currency": "RUR"
        }
    }


def test_vacancy_from_dict() -> None:
    v0 = Vacancy.from_dict(
        {
            "name": "name0",
            "snippet": {"requirement": "req0"},
            "alternate_url": "url0",
            "salary": {
                "from": 100,
                "to": 200,
                "currency": "RUR"
            }
        }
    )

    v1 = Vacancy(
        "name0", "req0", "url0",
        100, 200, "RUR"
    )

    assert v0.__dict__ == v1.__dict__

    with pytest.raises(KeyError):
        Vacancy.from_dict({"abobus": "bimbim"})
