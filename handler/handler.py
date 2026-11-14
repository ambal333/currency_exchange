from http.server import BaseHTTPRequestHandler

from Router.router import RouterPath
from controller.base_controller import BaseController


class RequestHandler(BaseHTTPRequestHandler):
    """Класс содержащий REST API методы

    Методы
    --------
    do_GET
        перенаправляет в контроллер и вызывает метод do_GET
    do_POST
        перенаправляет в контроллер и вызывает метод do_POST
    do_PATCH
        перенаправляет в контроллер и вызывает метод do_PATCH
    search_controller
        определяет путь запроса и возвращает соответствующий класс контроллера
    """

    def do_GET(self):
        try:
            controller: BaseController = self.search_controller()
            controller.do_GET()
        except Exception as e:
            self.send_error(400, 'not found')

    def do_POST(self):
        try:
            controller: BaseController = self.search_controller()
            controller.do_POST()
        except Exception as e:
            print('Такого пути нет')

    def do_PATCH(self):
        try:
            controller: BaseController = self.search_controller()
            controller.do_PATCH()
        except Exception as e:
            print('Такого пути нет')

    def search_controller(self):
        try:
            controller = RouterPath.search_path(self.path)
            return controller(self, self.server.database.connection)
        except Exception as e:
            print({'error': {e}})

    def do_DELETE(self):
        pass

    def end_headers(self):
        self.send_header(
            'Access-Control-Allow-Origin', '*'
        )
        self.send_header(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )
        self.send_header(
            'Access-Control-Allow-Headers', 'Content-Type'
        )
        super().end_headers()
