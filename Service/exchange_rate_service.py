from decimal import Decimal
from urllib.parse import unquote

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.App_error import CodeStandardError, ExchangeRateNotFound, \
    RateValidError, IntegrityError, NotExistExchangeRate
from DTO.exchange_rates_dto import ExchangeRatesDTO


class ExchangeRateService:
    __LENGTH_CODE = 3

    def __init__(self, connection):
        self.__dao = ExchangeRatesDao(connection)

    def get_unique_exchange_rate(self, two_code: str) -> dict:
        decod_cods = unquote(two_code)
        code_1 = decod_cods[:3]
        code_2 = decod_cods[3:]

        self.__validated_cods(code_1, code_2)

        exchange_rate = self.__dao.get_unique_exchange_rate(code_1, code_2)

        if exchange_rate:
            from_dto = ExchangeRatesDTO.get_exchange_rate(exchange_rate)
            return from_dto
        else:
            raise ExchangeRateNotFound(
                404,
                'Обменный курс для пары не найден'
            )

    def patch_exchange_rate(self, two_code: str, rate: Decimal) -> dict:
        decod_cods = unquote(two_code)
        code_1 = decod_cods[:3]
        code_2 = decod_cods[3:]

        self.__validated_cods(code_1, code_2)

        if rate <= 0:
            raise RateValidError(
                400,
                'курс не может быть меньше или равен 0'
            )

        self.__dao.patch_exchange_rates(
            code_1,
            code_2,
            rate
        )
        update_exchange_rate = self.__dao.get_unique_exchange_rate(code_1,
                                                                   code_2)
        if update_exchange_rate:
            from_dto = ExchangeRatesDTO.get_exchange_rate(update_exchange_rate)
        else:
            raise NotExistExchangeRate(
                404,
                'Валютная пара отсутствует в базе данных'
            )
        return from_dto

    def __validated_cods(self, code_1, code_2):
        if code_1 == code_2:
            raise IntegrityError(
                400,
                'Валюты не должны совпадать.'
            )

        if (len(code_1) != self.__LENGTH_CODE or len(code_2) !=
                self.__LENGTH_CODE):
            raise CodeStandardError(
                400,
                'Оба кода должны состоять из 3 символов.'
            )

        if code_1 != code_1.upper() or code_2 != code_2.upper():
            raise CodeStandardError(
                400,
                'Коды должны быть в верхнем регистре.'
            )

        if not ((code_1.isalpha() and code_1.isascii()) and
                code_2.isalpha() and code_2.isascii()):
            raise CodeStandardError(
                400,
                'Коды должны состоять из английских букв.'
            )
