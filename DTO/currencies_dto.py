from dataclasses import dataclass, asdict


@dataclass
class CurrenciesDTO:
    """Dataclass для формирования ответов REST API для валют.
    Атрибуты класса:
    ---------------
    id
        id валюты
    fullname
        название валюты
    code
        код валюты
    sign
        обозначение валюты
    Методы
    ------
    get_currency
        метод класса для формирования одной валюты
    get_currencies
        метод класса для формирования всех валют
    """
    id: int
    name: str
    code: str
    sign: str

    @classmethod
    def get_currency(cls, currency: tuple) -> dict:
        return asdict(cls(*currency))

    @classmethod
    def get_currencies(cls, currencies: list[tuple]) -> list[dict]:
        return [asdict(cls(*row)) for row in currencies]
