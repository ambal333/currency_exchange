import sqlite3
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from http.client import HTTPException
from urllib.parse import parse_qs

from Exception.App_error import DatabaseError, AppError
from Exception.App_error import FormFieldError
from Controller.base_controller import BaseController
from Service.exchange_rates_service import ExchangeRatesService


class ExchangeRatesController(BaseController):
    """Класс служит для получения конкретного обменного курса и добавления
    нового обменного курса в базу.

    Атрибуты
    --------
    Handler
        контроллер для обработки пути
    connection
        обеспечивает связь с бд
    __service
        экземпляр класса ExchangeRatesService для валидации и формирования
        ответа

    Методы
    ------
    do_GET
        обрабатывает запрос на получение всех обменных курсов из бд
    do_POST
        обрабатывает запрос на добавление нового обменного курса в бд
    do_PATCH
        генерирует исключение при обращении к методу
    """

    def __init__(self, handler, connection):
        super().__init__(handler, connection)
        self.service = ExchangeRatesService(connection)

    def do_GET(self):
        try:
            exchange_rates = self.service.get_exchange_rates()
            self.send_json(200, exchange_rates)

        except sqlite3.Error:
            raise DatabaseError(500, 'Ошибка базы данных')

    def do_POST(self):
        try:
            content_type = str(self.handler.headers.get(
                'Content-type')).split(';')[0].strip().lower()

            if content_type.strip() == 'application/x-www-form-urlencoded':
                content_length = int(
                    self.handler.headers.get('Content-length'))
                post_data = self.handler.rfile.read(content_length).decode(
                    'utf-8')
                param = parse_qs(post_data)
                if ('baseCurrencyCode' in param and 'targetCurrencyCode' in
                        param and 'rate' in param):
                    base_currency_code = param.get('baseCurrencyCode')[
                        0]
                    target_currency_code = param.get('targetCurrencyCode')[
                        0]
                    rate = Decimal(str(param.get('rate')[0])).quantize(
                        Decimal('0.000001'),
                        rounding=ROUND_HALF_UP)

                    unique_exchange_rates = (
                        self.service.post_exchange_rate(base_currency_code,
                                                        target_currency_code,
                                                        rate
                                                        ))

                    self.send_json(201, unique_exchange_rates)
                else:
                    raise FormFieldError(400, 'Отсутствует нужное поле формы')
        except InvalidOperation:
            self.send_error(
                400,
                'курс должен состоять из цифр'
            )
        except AppError as e:
            self.send_error(e.status_code, str(e))

        except Exception as e:
            self.send_error(501, str(e))

    def do_PATCH(self):
        try:
            raise HTTPException

        except Exception:
            self.send_error(501, 'Данный путь недоступен')
