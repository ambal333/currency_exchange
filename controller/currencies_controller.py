from http.client import HTTPException
from urllib.parse import parse_qs

from Exception.code_standart_error import CodeStandardError
from Exception.form_field_exception import FormFieldError
from controller.base_controller import BaseController
from DAO.currencies_dao import CurrenciesDao
from DTO.currencies_dto import CurrenciesDTO


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
    LENGTH_CODE = 3

    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.currencies_dao = CurrenciesDao(connection)

    def do_GET(self):
        try:
            currencies = self.currencies_dao.get_all_currencies()
            currencies_dto = CurrenciesDTO.get_currencies(currencies)
            self.send_json(200, currencies_dto)
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        try:
            content_type = str(self.handler.headers.get('Content-type', ''))
            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(
                    self.handler.headers.get('Content-length'))
                post_data = self.handler.rfile.read(content_length)
                data_decode = parse_qs(post_data.decode('utf-8'))

                if ('name' in data_decode and 'code' in data_decode and
                        'sign' in data_decode):
                    name = data_decode.get('name')[0]
                    code = data_decode.get('code')[0]
                    sign = data_decode.get('sign')[0]

                    if len(code) == self.LENGTH_CODE:
                        added_currency = self.currencies_dao.insert_currency(
                            code.upper(), name, sign)
                        added_currency_dto = CurrenciesDTO.get_currency(
                            added_currency)
                        self.send_json(200, added_currency_dto)
                    else:
                        raise CodeStandardError('Код не соответствует '
                                                'стандарту. ISO 4217 - 3 '
                                                'символа')
                else:
                    raise FormFieldError('Отсутствует нужное поле формы')
        except Exception as e:
            self.send_error(e)

    def do_PATCH(self):
        try:
            raise HTTPException
        except Exception as e:
            self.send_error(e)
