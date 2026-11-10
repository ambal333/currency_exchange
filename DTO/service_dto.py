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
    to_dict
        метод класса для формирования словаря
    """
    baseCurrency: dict
    targetCurrency: dict
    rate: Decimal
    amount: float
    convertedAmount: Decimal

    @classmethod
    def to_dict(cls, currency_exchange: tuple) -> dict:
        return asdict(cls(
            baseCurrency=CurrenciesDTO.from_tuple_to_dict(currency_exchange[
                                                              0]),
            targetCurrency=CurrenciesDTO.from_tuple_to_dict(
                currency_exchange[1]
            ),
            rate=currency_exchange[2],
            amount=currency_exchange[3],
            convertedAmount=currency_exchange[4]
        ))
