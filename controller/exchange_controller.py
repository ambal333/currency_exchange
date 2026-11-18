from decimal import InvalidOperation
from http.client import HTTPException
from urllib.parse import urlparse, parse_qs

from Exception.App_error import AppError, FormFieldError
from controller.base_controller import BaseController
from Service.service_exchange import ExchangeService
from Mappers.mapper_service import MapperService


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
            dict_param['code_from'] = path_parse.get('from')
            dict_param['code_to'] = path_parse.get('to')
            dict_param['amount'] = path_parse.get('amount')
            if None not in dict_param.values():
                dict_param = {
                    'code_from': dict_param['code_from'][0],
                    'code_to': dict_param['code_to'][0],
                    'amount': dict_param['amount'][0]
                }

                converted_amount, rate = ExchangeService(
                    self.connection).calculate_course(dict_param)

                convert_course = self.mapper.to_dto(
                    dict_param['code_from'],
                    dict_param['code_to'],
                    rate,
                    dict_param['amount'],
                    converted_amount
                )

                self.send_json(200, convert_course)

            else:
                raise FormFieldError(400, 'Отсутствует нужное поле формы')

        except InvalidOperation:
            self.send_error(
                400,
                'amount должен состоять из цифр'
            )

        except AppError as e:
            self.send_error(e.status_code, str(e))

    def do_POST(self):
        try:
            raise HTTPException
        except Exception:
            self.send_error(501, 'Данный путь недоступен')

    def do_PATCH(self):
        try:
            raise HTTPException
        except Exception:
            self.send_error(501, 'Данный путь недоступен')
