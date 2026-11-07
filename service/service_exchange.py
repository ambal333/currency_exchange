from decimal import Decimal, getcontext

from DAO.exchange_rates_dao import ExchangeRatesDao
from database.db_connection import DatabaseConnection
from DTO.exchange_rates_dto import ExchangeRatesDTO
class ExchangeRatesService:
    # __ctx = getcontext()
    # __ctx.prec = 1
    def __init__(self, connection: DatabaseConnection):
        self.__dao = ExchangeRatesDao(connection)

    def calculate_course(self, info: dict):
        exchange_rates = self.__dao.get_unique_exchange_rates(info.get(
            'code_from'), info.get('code_to'))

        if exchange_rates:
            exchange_rates_dto = ExchangeRatesDTO.from_tuple_to_dict(
                exchange_rates)
            rate = Decimal(str(exchange_rates_dto.get('rate')))
            amount = Decimal(str(info.get('amount')))
            converted_amount = rate * amount
            print(converted_amount)
            return converted_amount, rate
        exchange_rate_reverse = self.__dao.get_unique_exchange_rates(
            info.get('code_to'), info.get('code_from'))
        print(f'reverse:{exchange_rate_reverse}')

        if exchange_rate_reverse:
            exchange_rates_dto_reverse = ExchangeRatesDTO.from_tuple_to_dict(
                exchange_rate_reverse)
            # print(f'dto:{exchange_rates_dto_reverse}')
            rate = 1 / Decimal(str(exchange_rates_dto_reverse.get('rate')))
            amount = Decimal(str(info.get('amount')))
            print(f'rate= {rate}')
            print(f'amount= {amount}')
            converted_reverse_amount = Decimal(rate) * Decimal(amount)
            print(f'converted_reverse_amount'
                  f'= {float(converted_reverse_amount)}')
            return converted_reverse_amount, rate

        exchange_usd_from = self.__dao.get_unique_exchange_rates('USD',
                                                                     info.get('code_from'))
        exchange_usd_to = self.__dao.get_unique_exchange_rates('USD',
                                                                   info.get('code_to'))
        exchange_usd_from_dto = ExchangeRatesDTO.from_tuple_to_dict(exchange_usd_from)
        exchange_usd_to_dto = ExchangeRatesDTO.from_tuple_to_dict(exchange_usd_to)
        if exchange_usd_from and exchange_usd_to:
            rate_from = exchange_usd_from_dto.get('rate')
            rate_to = exchange_usd_to_dto.get('rate')
            rate_from_to = Decimal(rate_to) / Decimal(rate_from)
            convert_amount = Decimal(info.get('amount')) * rate_from_to
            return convert_amount, rate_from_to
        return None

    def direct_course(self, info):
        pass

    def reverse_course(self, info):
        pass

    def dollar_course(self, info: dict):
        pass

print(Decimal('0.011'))