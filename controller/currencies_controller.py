from controller.base_controller import BaseController
from DAO.currencies_dao import CurrenciesDao
class CurrenciesController(BaseController):
    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.currencies_dao = CurrenciesDao(connection)
    def do_GET(self):
        try:
            currencies = self.currencies_dao.get_all_currencies()
            print(currencies)
            self.send_json(200, currencies)
        except Exception as e:
            print({'error': e})
            return {'error': e}


    def do_POST(self):
        pass


