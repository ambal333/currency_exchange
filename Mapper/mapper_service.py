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
    get_bc_tc
        метод для получения базовой и целевой валют

    """

    def __init__(self, connection):
        self.__currencies_dao = CurrenciesDao(connection)

    def get_bc_tc(self, code_from, code_to):
        base_currency = self.__currencies_dao.get_unique_currency(code_from)
        target_currency = self.__currencies_dao.get_unique_currency(code_to)

        return base_currency, target_currency
