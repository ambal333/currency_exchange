from DAO.currencies_dao import CurrenciesDao
from Exception.App_error import CurrencyNotFound
from Database.db_connection import DatabaseConnection
from DTO.currencies_dto import CurrenciesDTO
from Service.Validated_codes import CheckCodes


class CurrencyService:
    """Класс используется для валидации, сериализации одной валюты

    Атрибуты
    --------
    __dao
        экземпляр класса CurrenciesDao, используется для получения и записи
        данных в бд

    Методы
    ------
    get_unique_currency
        валидация и получение уникальной валюты
    """

    def __init__(self, connection: DatabaseConnection):
        self.__dao = CurrenciesDao(connection)

    def get_unique_currency(self, code: str) -> dict:
        CheckCodes.validated_code_name(code)

        currency = self.__dao.get_unique_currency(code)

        if currency:
            from_dto = CurrenciesDTO.get_currency(currency)
            return from_dto
        else:
            raise CurrencyNotFound(
                404,
                'Валюта не найдена'
            )
