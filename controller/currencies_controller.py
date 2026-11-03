import sqlite3
from urllib.parse import parse_qs

from Exception.form_field_exception import FormFieldError
from controller.base_controller import BaseController
from DAO.currencies_dao import CurrenciesDao

class CurrenciesController(BaseController):
    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.currencies_dao = CurrenciesDao(connection)

    def do_GET(self):
        try:
            currencies = self.currencies_dao.get_all_currencies()
            self.send_json(200, currencies)
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        try:
            content_type = str(self.handler.headers.get('Content-type', ''))
            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers.get('Content-length'))
                post_data = self.handler.rfile.read(content_length)
                data_decode = parse_qs(post_data.decode('utf-8'))
                print(data_decode)
                if ('name' in data_decode and 'code' in data_decode and
                        'sign' in data_decode):
                    fullname = data_decode.get('name')[0]
                    code = data_decode.get('code')[0]
                    sign = data_decode.get('sign')[0]
                    added_currency = self.currencies_dao.insert_currency(
                        fullname, code, sign)
                    self.send_json(200, added_currency)
                else:
                    raise FormFieldError('Отсутствует нужное поле формы')
        except Exception as e:
            self.send_error(e)


