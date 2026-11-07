import json
import sqlite3

from Exception.code_standart_error import CodeStandardError
from Exception.exchange_rate_not_found import ExchangeRateNotFound
from Exception.exchange_rates_code_not_found import ExchangeRateCodeNotFound
from Exception.integrity_exchange_error import IntegrityExchangeError
from Exception.code_exception import CodeNotFoundError
from Exception.currency_not_found import CurrencyNotFound
from Exception.form_field_exception import FormFieldError
from Exception.not_exist_exchange_rate import NotExistExchangeRate
from Exception.not_exist_in_db import NotExistInDb
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
from database.db_connection import DatabaseConnection

class BaseController(ABC):
    def __init__(self, handler: BaseHTTPRequestHandler, connection: DatabaseConnection):
        self.handler = handler
        self.connection = connection
    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_POST(self):
        pass

    def do_PATCH(self):
        pass

    def send_json(self, status_code: int, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.handler.send_response(status_code)
        self.handler.send_header('content-type', 'application/json; charset=utf-8')
        self.handler.send_header('content-length', str(len(body)))
        self.handler.end_headers()
        self.handler.wfile.write(body)

    def send_error(self, error: Exception):
        try:
            if isinstance(error, FormFieldError):
                message = 'Отсутствует нужное поле формы'
                self.send_json(400, message)
            if isinstance(error, sqlite3.IntegrityError):
                message = 'Валюта с таким кодом уже существует'
                self.send_json(409, message)
            if isinstance(error, sqlite3.InternalError):
                message = 'база данных недоступна'
                self.send_json(500, message)
            if isinstance(error, CodeNotFoundError):
                message = 'Код валюты отсутствует в адресе'
                self.send_json(400, message)
            if isinstance(error, CurrencyNotFound):
                message = 'Валюта не найдена'
                self.send_json(404, message)
            if isinstance(error, NotExistInDb):
                message = 'Одна (или обе) валюта из валютной пары не существует в БД'
                self.send_json(404, message)
            if isinstance(error, IntegrityExchangeError):
                message = 'Валютная пара с таким кодом уже существует'
                self.send_json(409, message)
            if isinstance(error, NotExistExchangeRate):
                message = 'Валютная пара отсутствует в базе данных'
                self.send_json(404, message)
            if isinstance(error, ExchangeRateNotFound):
                message = 'Обменный курс для пары не найден'
                self.send_json(404, message)
            if isinstance(error, ExchangeRateCodeNotFound):
                message = 'Коды валют пары отсутствуют в адресе'
                self.send_json(400, message)
            if isinstance(error, CodeStandardError):
                message = ('Код не соответствует стандарту. ISO 4217 - 3 '
                           'символа')
        except Exception as e:
            self.send_json(400, e)