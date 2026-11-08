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
    from_tuple_to_dict
        метод класса для формирования одной валюты
    from_tuples_to_dict
        метод класса для формирования списка валют
    """

    id: int
    fullname: str
    code: str
    sign: str

    @classmethod
    def from_tuple_to_dict(cls, currency: tuple) -> dict:
        return asdict(cls(*currency))

    @classmethod
    def from_tuples_to_dict(cls, currencies: list[tuple]) -> list[dict]:
        return [asdict(cls(*row)) for row in currencies]
