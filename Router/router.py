from urllib.parse import urlparse

from controller.currencies_controller import CurrenciesController
from controller.currency_controller import CurrencyController
from controller.exchangeRates_controller import ExchangeRatesController
from controller.exchangeRate_controller import ExchangeRateController
from controller.service_controller import ServiceExchangeController

routes = {
    'currencies': CurrenciesController,
    'currency': CurrencyController,
    'exchangeRates': ExchangeRatesController,
    'exchangeRate': ExchangeRateController,
    'exchange': ServiceExchangeController
}


class RouterPath:
    """Класс служит для поиска пути запроса и определения соответствующего
    класса контроллера.

    Методы
    ------
    search_patch
        статический метод для поиска пути запроса

    """

    @staticmethod
    def search_path(request_path: str):
        path = urlparse(request_path).path
        split_path = path.split('/')
        if len(split_path) >= 2:
            route = split_path[1]
        else:
            route = '/'
        return routes.get(route)
