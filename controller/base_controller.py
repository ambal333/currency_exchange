import json
import sqlite3
from http.client import HTTPException

from Exception.code_standart_error import CodeStandardError
from Exception.exchange_rate_not_found import ExchangeRateNotFound
from Exception.exchange_rates_code_not_found import ExchangeRateCodeNotFound
from Exception.integrity_exchange_error import IntegrityExchangeError
from Exception.code_exception import CodeNotFoundError
from Exception.currency_not_found import CurrencyNotFound
from Exception.form_field_exception import FormFieldError
from Exception.not_exist_exchange_rate import NotExistExchangeRate
from Exception.currency_exchange_not_exist import CurrExchangeNotExist
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
from Exception.path_not_found import PathNotFound
from database.db_connection import DatabaseConnection


class BaseController(ABC):
    """Абстрактный базовый класс для всех контроллеров.

    Атрибуты
    --------
    handler: BaseHTTPRequestHandler
        Контроллер для обработки пути
    connection: DatabaseConnection
        Обеспечивает связь с бд

    Методы
    ------
    do_GET
        Абстрактный метод для обработки GET запроса
    do_POST
        Абстрактный метод для обработки POST запроса
    do_PATCH
        Абстрактный метод для обработки PATCH запроса
    send_json(self, status_code: int, data)
        Генерирует страницу для отправки ответа пользователю
    send_error(self, error: Exception)
        Метод для обработки ошибок
    """

    def __init__(self, handler: BaseHTTPRequestHandler,
                 connection: DatabaseConnection):
        self.handler = handler
        self.connection = connection

    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_POST(self):
        pass

    @abstractmethod
    def do_PATCH(self):
        pass

    def send_json(self, status_code: int, data: object) -> None:
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.handler.send_response(status_code)
        self.handler.send_header('content-type',
                                 'application/json; charset=utf-8')
        self.handler.send_header('content-length', str(len(body)))
        self.handler.end_headers()
        self.handler.wfile.write(body)

    def send_error(self, error: Exception) -> None:
        try:
            if isinstance(error, FormFieldError):
                message = {'message': 'Отсутствует нужное поле формы'}
                self.send_json(400, message)
            if isinstance(error, sqlite3.IntegrityError):
                message = {'message': 'Валюта с таким кодом уже существует'}
                self.send_json(409, message)
            if isinstance(error, sqlite3.InternalError):
                message = {'message': 'база данных недоступна'}
                self.send_json(500, message)
            if isinstance(error, CodeNotFoundError):
                message = {'message': 'Код валюты отсутствует в адресе'}
                self.send_json(400, message)
            if isinstance(error, CurrencyNotFound):
                message = {'message': 'Валюта не найдена'}
                self.send_json(404, message)
            if isinstance(error, CurrExchangeNotExist):
                message = ({'message': 'Одна (или обе) валюта из валютной пары'
                                       ' не существует в БД'})
                self.send_json(404, message)
            if isinstance(error, IntegrityExchangeError):
                message = {'message': 'Валютная пара с таким кодом уже '
                                      'существует'}
                self.send_json(409, message)
            if isinstance(error, NotExistExchangeRate):
                message = {'message': 'Валютная пара отсутствует в базе данных'}
                self.send_json(404, message)
            if isinstance(error, ExchangeRateNotFound):
                message = {'message': 'Обменный курс для пары не найден'}
                self.send_json(404, message)
            if isinstance(error, ExchangeRateCodeNotFound):
                message = {'message': 'Коды валют пары отсутствуют в адресе'}
                self.send_json(400, message)
            if isinstance(error, CodeStandardError):
                message = ({'message': 'Код не соответствует стандарту.'
                                       ' ISO 4217 - 3 символа'
                            })
                self.send_json(400, message)
            if isinstance(error, PathNotFound):
                message = {'message': 'Такого пути нет'}
                self.send_json(404, message)
            if isinstance(error, HTTPException):
                message = {'message': 'Некорректный запрос'}
                self.send_json(404, message)
        except Exception as e:
            self.send_json(400, {'message': e})
