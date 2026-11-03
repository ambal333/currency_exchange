
from Exception.code_exception import CodeNotFoundError
from Exception.currency_not_found import CurrencyNotFound
from controller.base_controller import BaseController
from DAO.currencies_dao import CurrenciesDao

class CurrencyController(BaseController):
    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.currency_dao = CurrenciesDao(connection)

    def do_GET(self):
        try:
            path = self.handler.path.split('/')[1:]
            if len(path) == 2 and path[1] != '':
                current_path, code = path
                unique_currency = self.currency_dao.get_unique_currency(
                    code.upper())
                if unique_currency is None:
                    raise CurrencyNotFound('Валюта не найдена')
                return self.send_json(200, unique_currency)
            else:
                raise CodeNotFoundError('Код валюты отсутствует в адресе')
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        pass