import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('content-type', 'application/json; charset=utf-8')
        self.send_header('content-length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):
        path = self.path
        status_code, data = self.server.router.dispatch('GET', path)
        self.send_json(status_code, data)
        print(data)

    def do_POST(self):
        responce_body = {}
        path = self.path
        content_length = int(self.headers['content-length'])
        data = self.rfile.read(content_length)
        body = parse_qs(data.decode('utf-8'))
        responce_body['name'] = body['name'][0]
        responce_body['code'] = body['code'][0]
        responce_body['sign'] = body['sign'][0]
        status_code, data_db = self.server.router.dispatch('POST', path, responce_body)
        self.send_json(status_code, data_db)
        print(body, path)

    def do_DELETE(self):
        pass