from dataclasses import dataclass, asdict
from decimal import Decimal

from DTO.currencies_dto import CurrenciesDTO
@dataclass
class ServiceDTO:
    baseCurrency: CurrenciesDTO
    targetCurrency: CurrenciesDTO
    rate: Decimal
    amount: float
    convertedAmount: Decimal

    @classmethod
    def to_dict(cls, currency_exchange: tuple) -> dict:
        return asdict(cls(
            baseCurrency=CurrenciesDTO.from_tuple_to_dict(currency_exchange[
                                                              0]),
            targetCurrency=CurrenciesDTO.from_tuple_to_dict(
                currency_exchange[1]),
            rate=currency_exchange[2],
            amount=currency_exchange[3],
            convertedAmount=currency_exchange[4]
        ))






