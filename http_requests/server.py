from http.server import BaseHTTPRequestHandler
from Router.router import RouterPath
from controller.base_controller import BaseController

class RequestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        controller: BaseController = self.search_controller()
        controller.do_GET()

    def do_POST(self):
        controller: BaseController = self.search_controller()
        controller.do_POST()

    def do_PATCH(self):
        controller: BaseController = self.search_controller()
        controller.do_PATCH()

    def search_controller(self):
        try:
            controller = RouterPath.search_path(self.path)
            return controller(self, self.server.database.connection)
        except Exception as e:
            print({'error': e})

    def do_DELETE(self):
        pass






