from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import unquote

from DAO.exchange_rates_dao import ExchangeRatesDao
from Exception.App_error import CodeStandardError, CourseNotExist, \
    IntegrityError, AmountError
from database.db_connection import DatabaseConnection
from DTO.exchange_rates_dto import ExchangeRatesDTO


class ExchangeService:
    """Класс служит для расчета конвертируемой валюты.
    Атрибуты
    --------
    __dao
        экземпляр класса дял работы с базой данных

    Методы
    ------
    calculate_course
        метод для выборки сценария расчета
    direct_course
        метод для расчета прямого сценария
    reverse_course
        метод для расчета обратного сценария
    course_from_usd
        метод для расчета сценария usd-a, usd-b
    """
    __LENGTH_CODE = 3

    def __init__(self, connection: DatabaseConnection):
        self.__dao = ExchangeRatesDao(connection)

    def calculate_course(self, info: dict):
        code_from = info.get('code_from')
        code_to = info.get('code_to')

        if ' ' in info['amount'] or not info['amount'].isdigit():
            raise AmountError(
                400,
                'параметр amount должен состоять из цифр.'
            )

        if float(info['amount']) < 0:
            raise AmountError(400,
                              'amount не может быть отрицательным')

        self.__validated_cods(code_from, code_to)

        exchange_rate = self.__dao.get_unique_exchange_rate(code_from, code_to)

        if exchange_rate:
            direct_course = self.direct_course(exchange_rate, info)
            return direct_course

        exchange_rate_reverse = self.__dao.get_unique_exchange_rate(code_to,
                                                                    code_from)

        if exchange_rate_reverse:
            reverse_course = self.reverse_course(exchange_rate_reverse, info)
            return reverse_course

        exchange_usd_from = self.__dao.get_unique_exchange_rate('USD',
                                                                code_from)
        exchange_usd_to = self.__dao.get_unique_exchange_rate('USD',
                                                              code_to)
        if exchange_usd_from and exchange_usd_to:
            course_from_usd = self.course_from_usd(
                exchange_usd_from,
                exchange_usd_to, info
            )
            return course_from_usd

        raise CourseNotExist(404,
                             'Обменный курс отсутствует в базе данных.'
                             )

    @staticmethod
    def direct_course(exchange_rate, info):
        exchange_rates_dto = ExchangeRatesDTO.get_exchange_rate(
            exchange_rate)
        rate = Decimal(str(exchange_rates_dto.get('rate')))
        amount = Decimal(str(info.get('amount')))
        converted_amount = (rate * amount)
        return (converted_amount.quantize(Decimal('0.01'),
                                          rounding=ROUND_HALF_UP),
                rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))

    @staticmethod
    def reverse_course(exchange_rate_reverse, info):
        exchange_rates_dto_reverse = ExchangeRatesDTO.get_exchange_rate(
            exchange_rate_reverse)
        rate = 1 / Decimal(str(exchange_rates_dto_reverse.get('rate')))
        amount = Decimal(str(info.get('amount')))
        converted_reverse_amount = (Decimal(rate) * Decimal(amount))
        return (converted_reverse_amount.quantize(Decimal('0.01'),
                                                  rounding=ROUND_HALF_UP),
                rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))

    @staticmethod
    def course_from_usd(exchange_usd_from, exchange_usd_to, info):
        exchange_usd_from_dto = ExchangeRatesDTO.get_exchange_rate(
            exchange_usd_from)
        exchange_usd_to_dto = ExchangeRatesDTO.get_exchange_rate(
            exchange_usd_to)
        rate_from = exchange_usd_from_dto.get('rate')
        rate_to = exchange_usd_to_dto.get('rate')
        rate_from_to = Decimal(str(rate_to)) / Decimal(str(rate_from))
        convert_amount = ((Decimal(str(info.get('amount'))) *
                           rate_from_to)).quantize(Decimal('0.01'),
                                                   rounding=ROUND_HALF_UP)
        return (convert_amount.quantize(Decimal('0.01'),
                                        rounding=ROUND_HALF_UP),
                rate_from_to.quantize(Decimal('0.000001'),
                                      rounding=ROUND_HALF_UP))

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
