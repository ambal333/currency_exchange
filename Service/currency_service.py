from urllib.parse import unquote

from DAO.currencies_dao import CurrenciesDao
from Exception.App_error import CodeStandardError, CurrencyNotFound
from database.db_connection import DatabaseConnection
from DTO.currencies_dto import CurrenciesDTO


class CurrencyService:
    __LENGTH_CODE = 3

    def __init__(self, connection: DatabaseConnection):
        self.__dao = CurrenciesDao(connection)

    def get_unique_currency(self, code: str) -> dict:
        if len(code) != self.__LENGTH_CODE:
            raise CodeStandardError(
                400,
                'Код должен состоять из 3 символов.'
            )

        if code != code.upper():
            raise CodeStandardError(
                400,
                'Код должен быть в верхнем регистре.'
            )

        decode_code = unquote(code)
        if not (code.isalpha() and decode_code.isascii()):
            raise CodeStandardError(
                400,
                'Код должен состоять из английских букв.'
            )
        currency = self.__dao.get_unique_currency(code)

        if currency:
            from_dto = CurrenciesDTO.get_currency(currency)
            return from_dto
        else:
            raise CurrencyNotFound(
                404,
                'Валюта не найдена'
            )
