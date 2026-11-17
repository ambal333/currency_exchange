from decimal import Decimal, ROUND_HALF_UP

from DAO.currencies_dao import CurrenciesDao
from DTO.service_dto import ServiceDTO


class MapperService:
    """Используется для определения базовой и целевой валют.

    Атрибуты
    ---------
    currencies_dao
        экземпляр класса, для получения уникальной валюты и бд
    Методы
    ------
    to_dto
        метод для получения базовой и целевой валют
    """

    def __init__(self, connection):
        self.__currencies_dao = CurrenciesDao(connection)

    def to_dto(self, code_from, code_to, rate: float, amount: str,
               converted_amount: Decimal) -> dict:
        base_currency = self.__currencies_dao.get_unique_currency(code_from)
        target_currency = self.__currencies_dao.get_unique_currency(code_to)
        exchange_rates_dto = ServiceDTO.get_exchange_rate((
            base_currency, target_currency,
            float(rate),
            float(Decimal(amount).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)),
            float(converted_amount)
        ))
        return exchange_rates_dto
