from dataclasses import dataclass, asdict
from decimal import Decimal

from DTO.currencies_dto import CurrenciesDTO


@dataclass
class ExchangeRatesDTO:
    """Dataclass используется для формирования готового ответа для REST API для
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
    get_exchange_rate
        метод класса для формирования одного обменного курса из бд
    get_exchange_rates
        метод класса для формирования всех обменных курсов из бд
    """
    id: int
    baseCurrency: dict
    targetCurrency: dict
    rate: Decimal

    @classmethod
    def get_exchange_rate(cls, exchange_rates: tuple) -> dict:
        return asdict(cls(
            id=exchange_rates[0],
            baseCurrency=CurrenciesDTO.get_currency(exchange_rates[
                                                               1:5]),
            targetCurrency=CurrenciesDTO.get_currency(
                exchange_rates[5:9]),
            rate=exchange_rates[9]
        ))

    @classmethod
    def get_exchange_rates(cls, exchange_rates: list[tuple]) -> list[dict]:
        return [cls.get_exchange_rate(row) for row in exchange_rates]
