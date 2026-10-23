
class Router:
    def __init__(self):
        self.routes = {}

    def add_routes(self, method, url, handler, code = None):
        if code is None:
            self.routes[(method.upper(), url)] = handler
        else:
            self.routes[(method.upper(), f'{url}/{code}')] = handler
    def dispatch(self, method, path):
        handler = self.routes.get((method.upper(), path))
        if handler is None:
            return 404, {'error': 'такого пути нет'}
        return handler()