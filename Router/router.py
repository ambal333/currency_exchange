from urllib.parse import urlparse

from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController

routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController,
    # 'exchangeRates': ExchangeRates,
    # 'exchangeRate': ExchangeRate,
    # 'exchange': Exchange
}

class RouterPath:

    @staticmethod
    def search_path(request_path: str):
        path = urlparse(request_path).path
        print(path)
        split_path = path.split('/')
        if len(split_path) >= 2:
            route = split_path[1]
        else:
            route = '/'
        return routes.get(route)
