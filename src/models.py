from src.abc_models import BaseModel


class Vacancy(BaseModel):
    name: str
    requirement: str | None

    url: str | None

    salary_from: int | None
    salary_to: int | None

    salary_currency: str | None

    # for comparing
    salary_mean: int | None

    __slots__ = (
        'name', 'requirement', 'url',
        'salary_from', 'salary_to', 'salary_currency', 'salary_mean'
    )

    def __init__(
            self, name: str, requirement: str | None = None, url: str | None = None,
            salary_from: int | None = None, salary_to: int | None = None,
            salary_currency: str | None = None
    ):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("A string expected for vacancy name")

        if not requirement or isinstance(requirement, str):
            self.requirement = requirement
        else:
            raise TypeError("A string expected for vacancy requirement")

        if not url or isinstance(url, str):
            self.url = url
        else:
            raise TypeError("A string expected for vacancy url")

        if salary_to:
            try:
                self.salary_to = int(salary_to)
            except TypeError:
                raise TypeError("Can't recognize salary_to as an integer")
        else:
            self.salary_to = None

        if salary_from:
            try:
                self.salary_from = int(salary_from)
            except TypeError:
                raise TypeError("Can't recognize salary_from as an integer")
        else:
            self.salary_from = None

        if not salary_currency or isinstance(salary_currency, str):
            self.salary_currency = salary_currency
        else:
            raise TypeError("A string expected for vacancy salary_currency")

        # for comparing
        if salary_to and salary_from:
            self.salary_mean = (salary_from + salary_to) // 2
        elif salary_to:
            self.salary_mean = salary_to
        elif salary_from:
            self.salary_mean = salary_from
        else:
            self.salary_mean = 0

    def __le__(self, other):
        return self.salary_mean <= other.salary_mean

    def __lt__(self, other):
        return self.salary_mean < other.salary_mean

    def __ge__(self, other):
        return self.salary_mean >= other.salary_mean

    def __gt__(self, other):
        return self.salary_mean > other.salary_mean

    @staticmethod
    def from_dict(data: dict):
        name = data['name']

        try:
            requirement = data['snippet']['requirement']
        except Exception:
            requirement = None

        url = data.get('alternate_url')

        salary = data.get('salary')

        if salary:
            salary_from = salary['from']
            salary_to = salary['to']
            salary_currency = salary['currency']
        else:
            salary_from = None
            salary_to = None
            salary_currency = None

        return Vacancy(
            name, requirement, url,
            salary_from, salary_to, salary_currency
        )

    def to_dict(self):
        return {
            'name': self.name,
            'snippet': {
                'requirement': self.requirement
            },
            'alternate_url': self.url,
            'salary': {
                'from': self.salary_from,
                'to': self.salary_to,
                'currency': self.salary_currency
            }
        }
