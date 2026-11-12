from dataclasses import dataclass, asdict
from decimal import Decimal

from DTO.currencies_dto import CurrenciesDTO


@dataclass
class ServiceDTO:
    """Dataclass класс для формирования ответа REST API для обмена валют.

    Атрибуты
    --------
    baseCurrency
        информация базовой валюты
    targetCurrency
        информация целевой валюты
    rate
        курс обмена
    amount
        количество валюты на обмен
    convertedAmount
        переведенная валюта

    Методы
    ------
    get_exchange_rate
        метод класса для формирования словаря
    """
    baseCurrency: dict
    targetCurrency: dict
    rate: float
    amount: float
    convertedAmount: float

    @classmethod
    def get_exchange_rate(cls, currency_exchange: tuple) -> dict:
        return asdict(cls(
            baseCurrency=CurrenciesDTO.get_currency(currency_exchange[
                                                              0]),
            targetCurrency=CurrenciesDTO.get_currency(
                currency_exchange[1]
            ),
            rate=currency_exchange[2],
            amount=currency_exchange[3],
            convertedAmount=currency_exchange[4]
        ))
