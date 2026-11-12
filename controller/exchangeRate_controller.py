from decimal import Decimal, ROUND_HALF_UP
from http.client import HTTPException
from urllib.parse import parse_qs

from Exception.exchange_rate_not_found import ExchangeRateNotFound
from Exception.exchange_rates_code_not_found import ExchangeRateCodeNotFound
from Exception.form_field_exception import FormFieldError
from Exception.not_exist_exchange_rate import NotExistExchangeRate
from controller.base_controller import BaseController
from DAO.exchange_rates_dao import ExchangeRatesDao
from DTO.exchange_rates_dto import ExchangeRatesDTO


class ExchangeRateController(BaseController):
    """Используется для получения конкретного и обновления существующего в базе
    обменных курсов.

    Атрибуты
    --------
    handler
        контроллер для обработки пути
    connection
        обеспечивает связь с бд
    dao
        экземпляр класса для получения и обновления обменных курсов в бд

    Методы
    ------
    do_GET
        обрабатывает запрос на получение конкретного обменного курса
    do_POST
        генерирует исключение, при обращении к методу
    do_PATCH
        обрабатывает запрос на обновление существующего обменного курса
    """

    def __init__(self, handler, connection):
        self.handler = handler
        super().__init__(handler, connection)
        self.dao = ExchangeRatesDao(connection)

    def do_GET(self):
        try:
            path = self.handler.path.split('/')[1:]
            if len(path) == 2 and path[1] != '':
                current_path, code = path
                code_1 = code[:3].upper()
                code_2 = code[3:].upper()
                unique_exchange_rate = (
                    self.dao.get_unique_exchange_rate(code_1, code_2))

                if unique_exchange_rate is None:
                    raise ExchangeRateNotFound(
                        'Обменный курс для пары не найден')

                unique_exchange_rate_dto = (
                    ExchangeRatesDTO.get_exchange_rate(unique_exchange_rate))
                return self.send_json(200, unique_exchange_rate_dto)
            else:
                raise ExchangeRateCodeNotFound(
                    'Коды валют пары отсутствуют в адресе')
        except Exception as e:
            self.send_error(e)

    def do_POST(self):
        try:
            raise HTTPException
        except Exception as e:
            self.send_error(e)

    def do_PATCH(self):
        try:
            path = self.handler.path.split('/')[1:]
            content_type = str(self.handler.headers.get('Content-type'))

            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers.get(
                    'content-length'))
                patch_data = self.handler.rfile.read(
                    content_length).decode('utf-8')
                dict_param = parse_qs(patch_data)

                if 'rate' in dict_param:
                    rate = Decimal(str(dict_param.get('rate')[0])).quantize(
                        Decimal('0.000001'),
                        rounding=ROUND_HALF_UP)

                    if len(path[1]) == 6:
                        code_1 = path[1][:3].upper()
                        code_2 = path[1][3:].upper()
                        self.dao.patch_exchange_rates(code_1, code_2, rate)
                        update_rates = (self.dao.get_unique_exchange_rate(
                            code_1, code_2))

                        rates_dto = ExchangeRatesDTO.get_exchange_rate(
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
