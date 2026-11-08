from http.client import HTTPException

from DTO.currencies_dto import CurrenciesDTO
from Exception.code_exception import CodeNotFoundError
from Exception.currency_not_found import CurrencyNotFound
from controller.base_controller import BaseController
from DAO.currencies_dao import CurrenciesDao


class CurrencyController(BaseController):
    """Используется для получения конкретной валюты.

    Атрибуты
    --------
    handler
        контроллер для обработки пути
    connection
        обеспечивает связь с бд

    Методы
    ------
    do_GET
        обрабатывает запрос на получение конкретной валюты
    do_POST
        генерирует исключение, при обращении к методу
    do_PATCH
        генерирует исключение, при обращении к методу
    """

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
                unique_currency_dto = CurrenciesDTO.from_tuple_to_dict(
                    unique_currency)
                return self.send_json(200, unique_currency_dto)
            else:
                raise CodeNotFoundError('Код валюты отсутствует в адресе')
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        try:
            raise HTTPException
        except Exception as e:
            self.send_error(e)

    def do_PATCH(self):
        try:
            raise HTTPException
        except Exception as e:
            self.send_error(e)
