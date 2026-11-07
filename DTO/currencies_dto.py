from dataclasses import dataclass, asdict
from decimal import Decimal

@dataclass
class CurrenciesDTO:
    id: int
    fullname: str
    code: str
    sign: str

    @classmethod
    def from_tuple_to_dict(cls, currency: tuple):
        return asdict(cls(*currency))

    @classmethod
    def from_tuples_to_dict(cls, currencies: list[tuple]):
        return [asdict(cls(*row)) for row in currencies]


rate = Decimal('0.012174336498660824')
amount = Decimal('1233.244')
print(rate * amount)