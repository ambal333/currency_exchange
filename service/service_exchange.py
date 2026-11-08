from decimal import Decimal, getcontext, ROUND_HALF_UP

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.currency_not_found import CurrencyNotFound
from database.db_connection import DatabaseConnection
from DTO.exchange_rates_dto import ExchangeRatesDTO
class ExchangeRatesService:
    def __init__(self, connection: DatabaseConnection):
        self.__dao = ExchangeRatesDao(connection)

    def calculate_course(self, info: dict):
        exchange_rate = self.__dao.get_unique_exchange_rate(info.get(
            'code_from'), info.get('code_to'))

        if exchange_rate:
            direct_course = self.direct_course(exchange_rate, info)
            return direct_course

        exchange_rate_reverse = self.__dao.get_unique_exchange_rate(
            info.get('code_to'), info.get('code_from'))

        if exchange_rate_reverse:
            reverse_curse = self.reverse_course(exchange_rate_reverse, info)
            return reverse_curse

        exchange_usd_from = self.__dao.get_unique_exchange_rate('USD',
                                                                info.get('code_from'))
        exchange_usd_to = self.__dao.get_unique_exchange_rate('USD',
                                                              info.get('code_to'))

        if exchange_usd_from and exchange_usd_to:
            course_from_usd = self.course_from_usd(exchange_usd_from,
                                            exchange_usd_to, info)
            return course_from_usd
        raise CurrencyNotFound('Валюта не найдена')


    def direct_course(self, exchange_rate, info):
        exchange_rates_dto = ExchangeRatesDTO.from_tuple_to_dict(
            exchange_rate)
        rate = Decimal(str(exchange_rates_dto.get('rate')))
        amount = Decimal(str(info.get('amount')))
        converted_amount = (rate * amount).quantize(Decimal('0.01'),
                                                    rounding=ROUND_HALF_UP)
        return converted_amount, rate.quantize(Decimal('0.01'),
                                               rounding=ROUND_HALF_UP)

    def reverse_course(self,exchange_rate_reverse, info):
        exchange_rates_dto_reverse = ExchangeRatesDTO.from_tuple_to_dict(
            exchange_rate_reverse)
        rate = 1 / Decimal(str(exchange_rates_dto_reverse.get('rate')))
        amount = Decimal(str(info.get('amount')))
        converted_reverse_amount = (Decimal(rate) * Decimal(amount)).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP)
        return converted_reverse_amount, rate.quantize(Decimal('0.01'),
                                                       rounding=ROUND_HALF_UP)

    def course_from_usd(self, exchange_usd_from, exchange_usd_to, info):
        exchange_usd_from_dto = ExchangeRatesDTO.from_tuple_to_dict(
            exchange_usd_from)
        exchange_usd_to_dto = ExchangeRatesDTO.from_tuple_to_dict(
            exchange_usd_to)
        rate_from = exchange_usd_from_dto.get('rate')
        rate_to = exchange_usd_to_dto.get('rate')
        rate_from_to = Decimal(str(rate_to)) / Decimal(str(rate_from))
        convert_amount = ((Decimal(str(info.get('amount'))) *
                           rate_from_to)).quantize(Decimal('0.01'),
                                                   rounding=ROUND_HALF_UP)
        round_rate_from_to = rate_from_to.quantize(Decimal('0.01'),
                                                   rounding=ROUND_HALF_UP)
        return convert_amount, round_rate_from_to