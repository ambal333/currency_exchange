from crud.get_all_currencies import get_all_curren
from crud.get_unique_currencies import get_unique_curren
from crud.insert_currencies import insert_currency
from crud.get_exchange_rates import get_exchange_rates
from crud.get_unique_exchange_rates import get_unique_exchange_rates
from crud.insert_exchange_rates import insert_exchange_rate
from crud.patch_exchange_rates import patch_exchange_rate
class Controller:
    def do_get_all(self):
        try:
            all_currencies = get_all_curren()
            if not all_currencies:
                return 404, {'error': 'в базе нет данных'}
            return 200, all_currencies
        except Exception:
            return 500, {'error':'база данных недоступна'}

    def do_get_unique(self,code):
        try:
            unique_currencies = get_unique_curren(code)
            if not unique_currencies:
                return 404, {'error': 'Валюта не найдена'}
            return 200, unique_currencies
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_post_currency(self, name, code, sign):
        try:
            status_code, db_post = insert_currency(code, name, sign)
            return status_code, db_post
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_get_exchange_rates(self):
        try:
            exchange_rates = get_exchange_rates()
            if not exchange_rates:
                return 404, {'error': 'в базе нет данных'}
            return 200, exchange_rates
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_get_unique_exchange_rates(self, code):
        try:
            code_1, code_2 = code[:3], code[3:]
            unique_exchange_rates = get_unique_exchange_rates(code_1, code_2)
            if not unique_exchange_rates:
                return 404, {'error': 'Обменный курс для пары не найден'}
            return 200, unique_exchange_rates
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_post_exchange_rates(self, baseCurrencyCode, targetCurrencyCode, rate):
        try:
            status_code, data = insert_exchange_rate(baseCurrencyCode,targetCurrencyCode, rate)
            return status_code, data
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_patch_exchange_currency(self, rate, code):
        try:
            code_1 = code[:3]
            code_2 = code[3:]
            data = patch_exchange_rate(rate, code_1, code_2)
            if not data:
                return 404, {'error': 'Валютная пара отсутствует в базе данных'}
            return 200, data
        except Exception:
            return 500, {'error': 'база данных недоступна'}