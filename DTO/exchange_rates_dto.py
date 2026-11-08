from dataclasses import dataclass, asdict
from decimal import Decimal

from DTO.currencies_dto import CurrenciesDTO


@dataclass
class ExchangeRatesDTO:
    """Используется для формирования готового ответа для REST API для
    обменных курсов.

    Атрибуты
    --------
    id
        id обменного курса
    baseCurrency
        информация базовой валюты
    targetCurrency
        информация целевой валюты
    rate
        курс обмена

    Методы
    ------
    from_tuple_to_dict
        метод класса для формирования одной валюты
    from_tuples_to_dict
        метод класса для формирования списка валют
    """
    id: int
    baseCurrency: dict
    targetCurrency: dict
    rate: Decimal

    @classmethod
    def from_tuple_to_dict(cls, exchange_rates: tuple) -> dict:
        return asdict(cls(
            id=exchange_rates[0],
            baseCurrency=CurrenciesDTO.from_tuple_to_dict(exchange_rates[1:5]),
            targetCurrency=CurrenciesDTO.from_tuple_to_dict(
                exchange_rates[5:9]),
            rate=exchange_rates[9]
        ))

    @classmethod
    def from_tuples_to_dict(cls, exchange_rates: list[tuple]) -> list[dict]:
        return [cls.from_tuple_to_dict(row) for row in exchange_rates]
