from urllib.parse import parse_qs

from Exception.form_field_exception import FormFieldError
from controller.base_controller import BaseController
from DAO.exchange_rates_dao import ExchangeRatesDao

class ExchangeRateController(BaseController):
    def __init__(self, handler, connection):
        self.handler = handler
        super().__init__(handler, connection)
        self.exchange_rate_dao = ExchangeRatesDao(connection)

    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PATCH(self):
        try:
            path = self.handler.path.split('/')[1:]
            print(path)
            content_type = str(self.handler.headers.get('Content-type'))
            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers.get(
                        'content-length'))
                patch_data = self.handler.rfile.read(
                        content_length).decode('utf-8')
                dict_param = parse_qs(patch_data)
                print(dict_param)
                if 'rate' in dict_param:
                    rate = float(dict_param.get('rate')[0])
                    if len(path[1]) == 6:
                        code_1 = path[1][:3].upper()
                        code_2 = path[1][3:].upper()
                        self.exchange_rate_dao.patch_exchange_rates(code_1, code_2, rate)
                    else:
                        pass
                else:
                    raise FormFieldError('Отсутствует нужное поле формы')
        except Exception as e:
            self.send_error(e)
