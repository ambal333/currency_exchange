from database.create_tables import init_database
from crud.insert_currencies import insert_currency
from crud.get_all_currencies import get_all_curren
from crud.get_unique_currencies import get_unique_curren
from crud.insert_exchange_rates import insert_exchange_rate
from http.server import HTTPServer
from http_requests.request_handler import RequestHandler
from controller.router import Router
from controller.controller import Controller
from crud.get_exchange_rates import get_exchange_rates
from crud.get_unique_exchange_rates import get_unique_exchange_rates
from crud.patch_exchange_rates import patch_exchange_rate


if __name__ == '__main__':
    init_database()
    router = Router()
    controller = Controller()
    router.add_routes('GET', '/currencies', controller.do_get_all)
    router.add_routes('GET', '/currencies/{code}', controller.do_get_unique)
    router.add_routes('POST', '/currencies', controller.do_post_currency)
    router.add_routes('GET', '/exchangeRates', controller.do_get_exchange_rates)
    router.add_routes('GET', '/exchangeRates/{code}', controller.do_get_unique_exchange_rates)
    router.add_routes('POST', '/exchangeRates', controller.do_post_exchange_rates)
    router.add_routes('PATCH', '/exchangeRate/{code}', controller.do_patch_exchange_rate)
    router.add_routes('GET', '/exchange?from={code_from}&to={code_to}&amount={amount}', controller.do_get_exchange_currency)
    # router.add_routes('GET', 'currencies', controller.do_get_unique)

    insert_currency('AUD','Australian dollar','A$')
    insert_currency('USD', 'American dollar', '$')
    # print(patch_exchange_rate(0.5, 'AUD', 'EUR'))
    # print(insert_exchange_rate('USD', 'AUD', 0.8))
    # print(get_unique_exchange_rates('AUD', 'USD'))
    # print(get_exchange_rates())
    # print(insert_exchange_rate('EUR', 'lir', 0.7))
    # print(insert_exchange_rate('RUB', 'AUD', 1.5))
    host, port = 'localhost', 8000
    server = HTTPServer((host,port), RequestHandler)
    server.router = router
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()