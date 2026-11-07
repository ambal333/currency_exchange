
from urllib.parse import urlparse, parse_qs
from controller.base_controller import BaseController
from service.service_exchange import ExchangeRatesService
from Exception.form_field_exception import FormFieldError
from DTO.service_dto import ServiceDTO
from Mapper.mapper_service import MapperService
class ServiceExchangeController(BaseController):
    def __init__(self, handler, connection):
        self.handler = handler
        self.mapper = MapperService(connection)
        super().__init__(handler, connection)

    def do_GET(self):
        dict_param = {'code_from': None, 'code_to': None, 'amount': None}
        try:
            path_str = urlparse(self.handler.path).query
            path_parse = parse_qs(urlparse(self.handler.path).query)
            print(f'path_parse = {path_parse}')
            print(path_str)
            dict_param['code_from'] = path_parse.get('from', None)
            dict_param['code_to'] = path_parse.get('to', None)
            dict_param['amount'] = path_parse.get('amount', None)
            print(f'dict_param: {dict_param}')
            if None not in dict_param.values():
                print('hello')
                dict_param = {'code_from': dict_param['code_from'][0].upper(),
                              'code_to': dict_param['code_to'][0].upper(),
                              'amount': dict_param['amount'][0].upper()}
                print(f'dict_param: {dict_param}')
                converted_amount = ExchangeRatesService(self.connection).calculate_course(dict_param)
                print(f'con_amount:{converted_amount}')
                exchange_rates_dto = self.mapper.get_dto_dict(dict_param['code_from'], dict_param['code_to'],
                             converted_amount[1], dict_param['amount'],
                             converted_amount[0])
                print(converted_amount[0])
                print(f'dto: {exchange_rates_dto}')
                self.send_json(200, exchange_rates_dto)
            else:
                raise FormFieldError('Отсутствует нужное поле формы')
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        pass