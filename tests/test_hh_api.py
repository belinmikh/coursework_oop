from typing import Any
from unittest.mock import patch

import pytest

from src.hh_api import HH


def test_hh_init() -> None:
    hh = HH()

    with pytest.raises(AttributeError):
        hh.__url
        hh.__headers
        hh.__params


@patch("requests.get")
def test_hh_get(get_mock: Any) -> None:
    get_mock.return_value.json.return_value = {
        "items": [
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
        ]
    }

    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    params = {"text": "abobus", "page": 0, "per_page": 100}

    expected = []

    for i in range(20):
        expected.append(
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

    hh = HH()

    assert hh.get("abobus") == expected

    get_mock.assert_called_with(url, headers=headers, params=params)
