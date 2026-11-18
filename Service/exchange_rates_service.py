from decimal import Decimal

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.App_error import RateValidError
from DTO.exchange_rates_dto import ExchangeRatesDTO
from Service.Validated_codes import CheckCodes


class ExchangeRatesService:
    """Класс используется для валидации и сериализации всех обменных курсов

    Атрибуты
    --------
    __dao
        экземпляр класса ExchangeRatesDao, используется для получения и записи
        данных в бд

    Методы
    ------
    get_exchange_rates
        валидация и получение всех обменных курсов
    post_exchange_rate
        валидация и добавление одного обменного курса в бд
    """
    def __init__(self, connection):
        self.__dao = ExchangeRatesDao(connection)

    def get_exchange_rates(self):
        exchange_rates = self.__dao.get_exchange_rates()
        from_dto = ExchangeRatesDTO.get_exchange_rates(exchange_rates)
        return from_dto

    def post_exchange_rate(self, base_currency_code: str,
                           target_currency_code: str, rate: Decimal) -> dict:

        CheckCodes.validated_cods(base_currency_code, target_currency_code)

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

