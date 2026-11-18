import json

from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
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

    def send_error(self, status_code: int, error: str) -> None:
        try:
            message = {'message': error}
            self.send_json(status_code, message)

        except Exception:
            self.send_json(501, {'message': 'Not found'})
