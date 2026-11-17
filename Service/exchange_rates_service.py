from decimal import Decimal
from urllib.parse import unquote

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.App_error import CodeStandardError, RateValidError, \
    IntegrityError
from DTO.exchange_rates_dto import ExchangeRatesDTO


class ExchangeRatesService:
    __LENGTH_CODE = 3

    def __init__(self, connection):
        self.__dao = ExchangeRatesDao(connection)

    def get_exchange_rates(self):
        exchange_rates = self.__dao.get_exchange_rates()
        from_dto = ExchangeRatesDTO.get_exchange_rates(exchange_rates)
        return from_dto

    def post_exchange_rate(self, base_currency_code: str,
                           target_currency_code: str, rate: Decimal) -> dict:

        self.__validated_cods(base_currency_code, target_currency_code)
        if rate <= 0:
            raise RateValidError(
                400,
                'курс не может быть меньше или равен 0'
            )

        exchange_rate = self.__dao.insert_exchange_rates(base_currency_code,
                                                         target_currency_code,
                                                         rate
                                                         )
        from_dto = ExchangeRatesDTO.get_exchange_rate(exchange_rate)
        return from_dto

    def __validated_cods(self, code_1, code_2):
        decode_code_1 = unquote(code_1)
        decode_code_2 = unquote(code_2)

        if decode_code_1 == decode_code_2:
            raise IntegrityError(
                400,
                'Валюты не должны совпадать.'
            )

        if (len(decode_code_1) != self.__LENGTH_CODE or len(decode_code_2) !=
                self.__LENGTH_CODE):
            raise CodeStandardError(
                400,
                'Оба кода должны состоять из 3 символов.'
            )

        if (decode_code_1 != decode_code_1.upper() or
                decode_code_2 != decode_code_2.upper()):
            raise CodeStandardError(
                400,
                'Коды должны быть в верхнем регистре.'
            )

        if not ((decode_code_1.isalpha() and decode_code_1.isascii()) and (
                decode_code_2.isalpha() and decode_code_2.isascii())):
            raise CodeStandardError(
                400,
                'Коды должны состоять из английских букв.'
            )
