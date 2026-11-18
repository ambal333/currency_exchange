import sqlite3
from http.client import HTTPException
from urllib.parse import parse_qs

from Exception.App_error import FormFieldError, DatabaseError, \
    AppError
from controller.base_controller import BaseController
from Service.currencies_service import CurrenciesService


class CurrenciesController(BaseController):
    """Используется для получения всех валют и добавления новой валюты в базу.

    Атрибуты
    --------
    handler
        контроллер для обработки пути
    currencies_dao
        экземпляр класса для работы с базой данных
    connection
        обеспечивает связь с бд

    Методы
    ------
    do_GET
        обрабатывает запрос на получение всех списка валют
    do_POST
        обрабатывает запрос на добавление новой валюты в базу
    do_PATCH
        генерирует исключение, при обращении к методу.
    """

    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.__service = CurrenciesService(connection)

    def do_GET(self):
        try:
            all_currencies = self.__service.get_all_currencies()
            self.send_json(200, all_currencies)
        except sqlite3.Error:
            raise DatabaseError(500, 'Ошибка базы данных')

    def do_POST(self):
        try:
            content_type = str(self.handler.headers.get(
                'Content-type', '')).split(';')[0].strip().lower()

            if content_type == 'application/x-www-form-urlencoded':
                content_length = int(
                    self.handler.headers.get('Content-length'))
                post_data = self.handler.rfile.read(content_length)
                data_decode = parse_qs(post_data.decode('utf-8'))

                if ('name' in data_decode and 'code' in data_decode and
                        'sign' in data_decode):
                    name = data_decode.get('name')[0]
                    code = data_decode.get('code')[0]
                    sign = data_decode.get('sign')[0]

                    added_currency = self.__service.post_currency(
                        code, name, sign
                    )
                    self.send_json(201, added_currency)

                else:
                    raise FormFieldError(
                        400,
                        'Отсутствует нужное поле формы'
                    )

        except AppError as e:
            self.send_error(e.status_code, str(e))

    def do_PATCH(self):
        try:
            raise HTTPException
        except HTTPException:
            self.send_json(501, {'message': 'Not found'})
