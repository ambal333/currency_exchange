from database.create_tables import init_database
from crud.insert_currencies import insert_currency
from crud.get_all_currencies import get_all_curren
from crud.get_unique_currencies import get_unique_curren
from http.server import HTTPServer
from http_requests.request_handler import RequestHandler
from controller.router import Router
from controller.controller import Controller
if __name__ == '__main__':
    init_database()
    router = Router()
    controller = Controller()
    router.add_routes('GET', '/currencies', controller.do_get_all)
    router.add_routes('GET', '/currencies/{code}', controller.do_get_unique)
    router.add_routes('POST', '/currencies', controller.do_post)
    # router.add_routes('GET', 'currencies', controller.do_get_unique)
    # insert_currency('AUD','Australian dollar','A$')
    insert_currency('USD', 'American dollar', '$')
    currency = get_all_curren()
    unique_currency = get_unique_curren('AU')
    host, port = 'localhost', 8000
    server = HTTPServer((host,port), RequestHandler)
    server.router = router
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()