import json
from http.server import BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path.lstrip('/')
        status_code, data = self.server.router.dispatch('GET', path)
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('content-type', 'application/json; charset=utf-8')
        self.send_header('content-length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(data)
    def do_POST(self):
        pass
    def do_DELETE(self):
        pass