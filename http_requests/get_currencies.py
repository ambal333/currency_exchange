from http.server import HTTPServer, BaseHTTPRequestHandler

class GetCurrencies(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip('/')
        if path:
            self.send_response(200)
