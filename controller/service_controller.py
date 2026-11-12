from decimal import Decimal, ROUND_HALF_UP
from http.client import HTTPException
from urllib.parse import urlparse, parse_qs

from controller.base_controller import BaseController
from service.service_exchange import ExchangeRatesService
from Exception.form_field_exception import FormFieldError
from Mappers.mapper_service import MapperService
from DTO.service_dto import ServiceDTO


class ServiceExchangeController(BaseController):
    """Класс служит для перевода определённого количества средств из одной
    валюты в другую.

    Атрибуты
    --------
    handler
        контроллер для обработки пути
    connection
        обеспечивает связь с бд
    mapper
        экземпляр класса для получения сформированного словаря с данными

    Методы
    ------
    do_GET
        обрабатывает запрос на перевод определённого количества средств из
        одной валюты в другую
    do_POST
        генерирует исключение при обращении к методу
    do_PATCH
        генерирует исключение при обращении к методу
    """

    def __init__(self, handler, connection):
        self.handler = handler
        self.mapper = MapperService(connection)
        super().__init__(handler, connection)

    def do_GET(self):
        dict_param = {'code_from': None,
                      'code_to': None,
                      'amount': None
                      }
        try:
            path_parse = parse_qs(urlparse(self.handler.path).query)
            dict_param['code_from'] = path_parse.get('from', None)
            dict_param['code_to'] = path_parse.get('to', None)
            dict_param['amount'] = path_parse.get('amount', None)

            if None not in dict_param.values():
                dict_param = {
                    'code_from': dict_param['code_from'][0].upper(),
                    'code_to': dict_param['code_to'][0].upper(),
                    'amount': dict_param['amount'][0]
                }
                converted_amount, rate = ExchangeRatesService(
                    self.connection).calculate_course(dict_param)

                # конвертируем средства из одной валюту в другую
                base_currency, target_currency = self.mapper.to_dto(
                    dict_param['code_from'],
                    dict_param['code_to'])

                exchange_rates_dto = ServiceDTO.get_exchange_rate((
                    base_currency, target_currency,
                    float(rate),
                    float(Decimal(dict_param['amount']).quantize(Decimal(
                        '0.01'),
                                                   rounding=ROUND_HALF_UP)),
                    float(converted_amount)
                ))

                self.send_json(200, exchange_rates_dto)
            else:
                raise FormFieldError('Отсутствует нужное поле формы')

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
