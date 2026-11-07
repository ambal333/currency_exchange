from urllib.parse import parse_qs

from Exception.exchange_rate_not_found import ExchangeRateNotFound
from Exception.exchange_rates_code_not_found import ExchangeRateCodeNotFound
from Exception.form_field_exception import FormFieldError
from Exception.not_exist_exchange_rate import NotExistExchangeRate
from controller.base_controller import BaseController
from DAO.exchange_rates_dao import ExchangeRatesDao
from DTO.exchange_rates_dto import ExchangeRatesDTO


class ExchangeRateController(BaseController):
    def __init__(self, handler, connection):
        self.handler = handler
        super().__init__(handler, connection)
        self.exchange_rate_dao = ExchangeRatesDao(connection)

    def do_GET(self):
        try:
            path = self.handler.path.split('/')[1:]

            if len(path) == 2 and path[1] != '':
                current_path, code = path
                code_1 = code[:3].upper()
                code_2 = code[3:].upper()
                unique_exchange_rate = (
                    self.exchange_rate_dao.get_unique_exchange_rates(code_1,
                                                                     code_2))
                if unique_exchange_rate is None:
                    raise ExchangeRateNotFound(
                        'Обменный курс для пары не найден')
                print(unique_exchange_rate)
                unique_exchange_rate_dto = (
                    ExchangeRatesDTO.from_tuple_to_dict(unique_exchange_rate))
                return self.send_json(200, unique_exchange_rate_dto)
            else:
                raise ExchangeRateCodeNotFound(
                    'Коды валют пары отсутствуют в адресе')
        except Exception as e:
            self.send_error(e)

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
                        self.exchange_rate_dao.patch_exchange_rates(code_1,
                                                                    code_2,
                                                                    rate)
                        update_rates = self.exchange_rate_dao.get_unique_exchange_rates(
                            code_1, code_2)
                        rates_dto = ExchangeRatesDTO.from_tuple_to_dict(
                            update_rates
                        )
                        self.send_json(200, rates_dto)
                    else:
                        raise NotExistExchangeRate(
                            'Валютная пара отсутствует в базе данных'
                        )
                else:
                    raise FormFieldError('Отсутствует нужное поле формы')
        except Exception as e:
            self.send_error(e)
