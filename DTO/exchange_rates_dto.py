from dataclasses import dataclass, asdict
from decimal import Decimal

from DTO.currencies_dto import CurrenciesDTO


@dataclass
class ExchangeRatesDTO:
    id: int
    baseCurrency: CurrenciesDTO
    targetCurrency: CurrenciesDTO
    rate: Decimal

    @classmethod
    def from_tuple_to_dict(cls, exchange_rates: tuple):
        print(exchange_rates)
        return asdict(cls(
            id=exchange_rates[0],
            baseCurrency=CurrenciesDTO.from_tuple_to_dict(exchange_rates[1:5]),
            targetCurrency=CurrenciesDTO.from_tuple_to_dict(exchange_rates[5:9]),
            rate=exchange_rates[9]
        ))

    @classmethod
    def from_tuples_to_dict(cls, exchange_rates: list[tuple]):
        return [cls.from_tuple_to_dict(row) for row in exchange_rates]