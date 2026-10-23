from crud.get_all_currencies import get_all_curren

class Controller:
    def do_get_all(self):
        try:
            all_currencies = get_all_curren()
            if not all_currencies:
                return 404, {'error': 'в базе нет данных'}
            return 200, all_currencies
        except Exception:
            return 500, {'error':'база данных недоступна'}

    def do_get_unique(self):
        pass

