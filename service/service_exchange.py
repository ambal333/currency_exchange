from decimal import Decimal, getcontext

from DAO.exchange_rates_dao import ExchangeRatesDao
from database.db_connection import DatabaseConnection
class ExchangeRatesService:
    ctx = getcontext()
    ctx.prec = 2
    def __init__(self, connection: DatabaseConnection):
        self.dao = ExchangeRatesDao(connection)

    def calculate_course(self, info: dict):
        exchange_rates = self.dao.get_unique_exchange_rates(info.get('code_from'), info.get('code_to'))

        if exchange_rates:
            rate = Decimal(str(exchange_rates.get('rate')))
            amount = Decimal(str(info.get('amount')))
            converted_amount = rate * amount
            return converted_amount

        exchange_rate_reverse = self.dao.get_unique_exchange_rates(info.get('code-to'), info.get('code_from'))

        if exchange_rate_reverse:
            rate = 1 / Decimal(str(exchange_rates.get('rate')))
            amount = Decimal(str(info.get('amount')))
            converted_reverse_amount = rate * amount
            return converted_reverse_amount

        exchange_rate_usd_from = self.dao.get_unique_exchange_rates('USD', info.get('code_from'))
        exchange_rate_usd_to = self.dao.get_unique_exchange_rates('USD', info.get('code_to'))

        if exchange_rate_usd_from and exchange_rate_usd_to:
            rate_from = exchange_rate_usd_from.get('rate')
            rate_to = exchange_rate_usd_to.get('rate')
            rate_from_to = Decimal(rate_to) / Decimal(rate_from)
            convert_amount = info.get('amount') * rate_from_to
            return convert_amount

    def direct_course(self, info):
        pass

    def reverse_course(self, info):
        pass

    def dollar_course(self, info: dict):
        pass