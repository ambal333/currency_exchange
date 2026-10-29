from crud.get_all_currencies import get_all_curren
from crud.get_unique_currencies import get_unique_curren
from crud.insert_currencies import insert_currency
from crud.get_exchange_rates import get_exchange_rates
from crud.get_unique_exchange_rates import get_unique_exchange_rates
from crud.insert_exchange_rates import insert_exchange_rate
from crud.patch_exchange_rates import patch_exchange_rate
from crud.get_unique_exchange_rates import get_unique_exchange_rates
from crud.format_data import format_exchange_currency
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
            print(baseCurrencyCode)
            status_code, data = insert_exchange_rate(baseCurrencyCode,targetCurrencyCode, rate)
            return status_code, data
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_patch_exchange_rate(self, rate, code):
        try:
            code_1 = code[:3]
            code_2 = code[3:]
            data = patch_exchange_rate(rate, code_1, code_2)
            if not data:
                return 404, {'error': 'Валютная пара отсутствует в базе данных'}
            return 200, data
        except Exception:
            return 500, {'error': 'база данных недоступна'}

    def do_get_exchange_currency(self, code_from, code_to, amount):
        try:
            exchange_rate = get_unique_exchange_rates(code_from, code_to)
            if exchange_rate:
                converted_amount = float(exchange_rate['rate']) * float(amount)
                exchange_rate['amount'] = amount
                exchange_rate['convertedAmount'] = converted_amount
                return 200, exchange_rate
            exchange_rate_reverse = get_unique_exchange_rates(code_to, code_from)
            if exchange_rate_reverse:
                rate = float(exchange_rate_reverse.get('rate'))
                converted_rate = round((1 / rate), 4)
                converted_amount_reverse = round(converted_rate, 4) * round(float(amount),4)
                res = format_exchange_currency(exchange_rate_reverse.get('baseCurrency'),
                                         exchange_rate_reverse.get('targetCurrency'),
                                         converted_rate, amount, converted_amount_reverse)
                return 200, res
            exchange_rate_usd_from = get_unique_exchange_rates('USD', code_from)
            exchange_rate_usd_to = get_unique_exchange_rates('USD', code_to)
            if exchange_rate_usd_from and exchange_rate_usd_to:
                rate_from = exchange_rate_usd_from['rate']
                rate_to = exchange_rate_usd_to['rate']
                rate_from_to = round((rate_to / rate_from), 4)
                convert_amount = float(amount) * rate_from_to
                res = format_exchange_currency(exchange_rate_usd_from['targetCurrency'],
                                               exchange_rate_usd_to['targetCurrency'],
                                               rate_from_to, amount,
                                               convert_amount)
                return 200, res
            else:
                return 404, {'error': 'Валютная пара отсутствует в базе данных'}
        except Exception:
            return 500, {'error': 'база данных недоступна'}