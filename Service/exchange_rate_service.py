from decimal import Decimal
from urllib.parse import unquote

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.App_error import (ExchangeRateNotFound,
                                 RateValidError,
                                 NotExistExchangeRate)
from DTO.exchange_rates_dto import ExchangeRatesDTO
from Service.Validated_codes import CheckCodes


class ExchangeRateService:
    """Класс используется для валидации, сериализации обменных курсов

    Атрибуты
    --------
    __dao
        экземпляр класса ExchangeRatesDao, используется для получения и записи
        данных в бд

    Методы
    ------
    get_unique_exchange_rate
        валидация и получения одного обменного курса
    patch_exchange_rate
        валидация и обновление rate в обменном курсе
    """

    def __init__(self, connection):
        self.__dao = ExchangeRatesDao(connection)

    def get_unique_exchange_rate(self, two_code: str) -> dict:
        decod_cods = unquote(two_code)
        code_1 = decod_cods[:3]
        code_2 = decod_cods[3:]

        CheckCodes.validated_cods(code_1, code_2)

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

        CheckCodes.validated_cods(code_1, code_2)

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
