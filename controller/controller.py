from crud.get_all_currencies import get_all_curren
from crud.get_unique_currencies import get_unique_curren
from crud.insert_currencies import insert_currency
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
        pass
