import sqlite3
from urllib.parse import unquote

from DAO.currencies_dao import CurrenciesDao
from DTO.currencies_dto import CurrenciesDTO
from Exception.App_error import (CodeStandardError,
                                 NameStandardError,
                                 IntegrityError)
from database.db_connection import DatabaseConnection


class CurrenciesService:
    __LENGTH_CODE = 3

    def __init__(self, connection: DatabaseConnection):
        self.__dao = CurrenciesDao(connection)

    def get_all_currencies(self) -> list[dict]:
        currencies = self.__dao.get_all_currencies()
        currencies_dto = CurrenciesDTO.get_currencies(currencies)
        return currencies_dto

    def post_currency(self, code: str, name: str, sign: str) -> dict:
        try:
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
            decode_name = unquote(name)
            if not (decode_name.isascii()):
                raise NameStandardError(
                    400,
                    'Название валюты должно состоять из '
                    'английских символов.'
                )

            added_currency = self.__dao.insert_currency(code, name, sign)
            from_dto = CurrenciesDTO.get_currency(added_currency)
            return from_dto

        except sqlite3.IntegrityError:
            raise IntegrityError(
                409,
                'Валюта с таким кодом уже существует'
            )
