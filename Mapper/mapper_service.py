from DAO.currencies_dao import CurrenciesDao
from DTO.service_dto import ServiceDTO


class MapperService:
    def __init__(self, connection):
        self.currencies_dao = CurrenciesDao(connection)

    def get_dto_dict(self, code_from, code_to, rate, amount, converted_amount):
        baseCurrency = self.currencies_dao.get_unique_currency(code_from)
        targetCurrency = self.currencies_dao.get_unique_currency(code_to)

        exchange_rate_dto = ServiceDTO.to_dict((baseCurrency, targetCurrency,
                                                float(rate), amount,
                                                float(converted_amount)))
        return exchange_rate_dto
