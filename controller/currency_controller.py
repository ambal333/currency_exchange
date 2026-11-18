from http.client import HTTPException

from Exception.App_error import AppError
from Exception.App_error import CodeNotFoundError
from controller.base_controller import BaseController
from Service.currency_service import CurrencyService


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
        self.__service = CurrencyService(connection)

    def do_GET(self):
        try:
            path = self.handler.path.split('/')[1:]
            if len(path) == 2 and path[1] != '':
                current_path, code = path

                unique_currency = self.__service.get_unique_currency(
                    code)

                return self.send_json(200, unique_currency)
            else:
                raise CodeNotFoundError(400, 'Код валюты отсутствует в адресе')
        except AppError as e:
            self.send_error(e.status_code, str(e))

    def do_POST(self):
        try:
            raise HTTPException
        except HTTPException:
            self.send_json(501, {'message': 'Not found'})

    def do_PATCH(self):
        try:
            raise HTTPException
        except HTTPException:
            self.send_json(501, {'message': 'Not found'})
