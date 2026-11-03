import json
from urllib.parse import parse_qs
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




    # def do_GET(self):
    #     path = self.path
    #     status_code, data = self.server.router.dispatch('GET', path)
    #     self.send_json(status_code, data)
    #
    # def do_POST(self):
    #     response_body = {}
    #     path = self.path
    #     content_length = int(self.headers['content-length'])
    #     data = self.rfile.read(content_length)
    #     body = parse_qs(data.decode('utf-8'))
    #     if 'name' in body and 'code' in body and 'sign' in body:
    #         response_body['name'] = body['name'][0]
    #         response_body['code'] = body['code'][0]
    #         response_body['sign'] = body['sign'][0]
    #         status_code, data_db = self.server.router.dispatch('POST', path, response_body)
    #         self.send_json(status_code, data_db)
    #     if 'baseCurrencyCode' in body and 'targetCurrencyCode' in body and 'rate' in body:
    #         response_body['targetCurrencyCode'] = body['targetCurrencyCode'][0]
    #         response_body['baseCurrencyCode'] = body['baseCurrencyCode'][0]
    #         print(body['targetCurrencyCode'][0],body['baseCurrencyCode'][0])
    #         response_body['rate'] = body['rate'][0]
    #         status_code, data_db = self.server.router.dispatch('POST', path, response_body)
    #         self.send_json(status_code, data_db)
    #     else:
    #         self.send_json(400,{'error': 'Отсутствует нужное поле формы'})
    # def do_PATCH(self):
    #     new_rate = {}
    #     path = self.path
    #     content_length = int(self.headers['content-length'])
    #     data = self.rfile.read(content_length)
    #     body = parse_qs(data.decode('utf-8'))
    #     if 'rate' in body:
    #         new_rate['rate'] = body['rate'][0]
    #         status_code, update_rate = self.server.router.dispatch('PATCH', path, new_rate)
    #         self.send_json(status_code, update_rate)






