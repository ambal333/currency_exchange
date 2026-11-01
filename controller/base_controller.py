import json

from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler

class BaseController(ABC):
    def __init__(self, handler: BaseHTTPRequestHandler, connection):
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

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.handler.send_response(status_code)
        self.handler.send_header('content-type', 'application/json; charset=utf-8')
        self.handler.send_header('content-length', str(len(body)))
        self.handler.end_headers()
        self.handler.wfile.write(body)