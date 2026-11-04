from Exception.form_field_exception import FormFieldError
from controller.base_controller import BaseController
from DAO.exchange_rates_dao import ExchangeRatesDao
from urllib.parse import parse_qs
class ExchangeRatesController(BaseController):
    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.exchange_rates_dao = ExchangeRatesDao(connection)

    def do_GET(self):
        try:
            exchange_rates = self.exchange_rates_dao.get_exchange_rates()
            self.send_json(200, exchange_rates)
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        try:
            content_type = str(self.handler.headers.get('Content-type'))
            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers.get('Content-length'))
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                param = parse_qs(post_data)
                if ('baseCurrencyCode' in param and 'targetCurrencyCode' in
                        param and 'rate' in param):
                    basecurrency_code = param.get('baseCurrencyCode')[0]
                    target_currency_code = param.get('targetCurrencyCode')[0]
                    rate = float(param.get('rate')[0])
                    self.exchange_rates_dao.insert_exchange_rates(
                        basecurrency_code, target_currency_code, rate)
                else:
                    raise FormFieldError('Отсутствует нужное поле формы')

        except Exception as e:
            self.send_error(e)

