from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from http.client import HTTPException
from urllib.parse import parse_qs

from Exception.App_error import ExchangeRateCodeNotFound, AppError, \
    FormatFormError
from Exception.App_error import FormFieldError
from Controller.base_controller import BaseController
from Service.exchange_rate_service import ExchangeRateService


class ExchangeRateController(BaseController):
    """Используется для получения конкретного и обновления существующего в базе
    обменных курсов.

    Атрибуты
    --------
    Handler
        контроллер для обработки пути
    connection
        обеспечивает связь с бд
    __service
        экземпляр класса ExchangeRateService для валидации и формирования
        ответа

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
        super().__init__(handler, connection)
        self.__service = ExchangeRateService(connection)

    def do_GET(self):
        try:
            path = self.handler.path.split('/')[1:]
            if len(path) == 2 and path[1] != '':
                current_path, codes = path

                unique_exchange_rate = (
                    self.__service.get_unique_exchange_rate(codes)
                )

                return self.send_json(200, unique_exchange_rate)

            else:
                raise ExchangeRateCodeNotFound(
                    400,
                    'Коды валют пары отсутствуют в адресе'
                )
        except AppError as e:
            self.send_error(e.status_code, str(e))

    def do_POST(self):
        try:
            raise HTTPException
        except HTTPException:
            self.send_json(501, {'message': 'Not found'})

    def do_PATCH(self):
        try:
            path = self.handler.path.split('/')[1:]
            content_type = str(self.handler.headers.get(
                'Content-type')).split(';')[0].strip().lower()

            if content_type == 'application/x-www-form-urlencoded':
                content_length = int(self.handler.headers.get(
                    'content-length'))
                patch_data = self.handler.rfile.read(
                    content_length).decode('utf-8')
                dict_param = parse_qs(patch_data)
                print(dict_param)
                if 'rate' in dict_param and dict_param.get('rate') != '':
                    rate = Decimal(str(dict_param.get('rate')[0])).quantize(
                        Decimal('0.000001'),
                        rounding=ROUND_HALF_UP)

                    update_exchange_rates = (
                        self.__service.patch_exchange_rate(
                            path[1], rate
                        ))

                    self.send_json(200, update_exchange_rates)
                else:
                    raise FormFieldError(
                        400,
                        'Отсутствует нужное поле формы'
                    )
            else:
                raise FormatFormError(
                    415,
                    'Неверный формат полей.'
                )
        except InvalidOperation:
            self.send_error(
                400,
                'курс должен состоять из цифр'
            )
        except AppError as e:
            self.send_error(e.status_code, str(e))
