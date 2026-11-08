from http.server import BaseHTTPRequestHandler

from Router.router import RouterPath
from controller.base_controller import BaseController


class RequestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            controller: BaseController = self.search_controller()
            controller.do_GET()
        except Exception as e:
            print('Такого пути нет')

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
            print(f'error: {e}')

    def do_DELETE(self):
        pass






