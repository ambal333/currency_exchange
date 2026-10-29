import re

class Router:
    def __init__(self):
        self.routes = {}

    def add_routes(self, method, url, handler):
        self.routes[(method.upper(), url)] = handler

    def dispatch(self, method, path, data=None):
        current_path, code= self.search_path(path, method)
        # print(current_path)
        handler = self.routes.get((method.upper(), current_path))
        if handler is None:
            return 404, {'error': 'такого пути нет'}
        if 'code' in code:
            if code.get('code') != '' and code.get('method') != 'PATCH':
                current_code = code.get('code')
                return handler(current_code)
            elif code.get('code') == '':
                return 400, {'error': 'Код валюты отсутствует в адресе'}
        if code.get('method') == 'POST':
            return handler(**data)
        if code.get('method') == 'PATCH':
            data['code'] = code['code']
            return handler(**data)
        if 'amount' in code:
            info = {'code_from': code.get('code_from'), 'code_to': code.get('code_to'), 'amount': code.get('amount')}
            return handler(**info)
        else:
            return handler()

    def search_path(self, path, method):
        # find_path = path.split('/')[1::]
        find_path = re.split(r'[/?=&]', path)[1::]
        # print(find_path)
        for key, value in self.routes.items():
            flag = 0
            code = {}
            save_path = re.split(r'[/?=&]', key[1])[1::]
            # print(save_path)
            current_method = key[0]
            if len(find_path) == len(save_path):
                if method == current_method:
                    for index, i in enumerate(find_path):
                        if save_path[index] == i:
                            flag = 1
                        if save_path[index].startswith('{') and save_path[index].endswith('}'):
                            code[save_path[index][1:-1]] = i.upper()
                        code['method'] = method.upper()
                    if flag == 1:
                        return key[1], code
                else:
                    continue
            else:
                continue
        return 'нет подходящего пути'

router = Router()
router.add_routes('GET', '/currencies', None)
router.add_routes('GET', '/currencies/{code}', None)
router.add_routes('POST', '/currencies', None)
router.add_routes('GET', '/exchangeRates', None)
router.add_routes('GET', '/exchangeRates/{code}', None)
router.add_routes('POST', '/exchangeRates', None)
router.add_routes('PATCH', '/exchangeRate/{code}', None)
router.add_routes('GET', '/exchange?from={code_from}&to={code_to}&amount={amount}', None) #/exchange?from=USD&to=AUD&amount=10
print(router.search_path('/exchange?from=USD&to=AUD&amount=10', 'GET')) #('/currencies/{code}', {'code': 'EUR'})
# print(router.search_path('/currencies/eur', 'GET')) #('/currencies/{code}', {'code': 'EUR'})
# print(router.search_path('/currencies', 'GET')) #('/currencies', {})
# print(router.search_path('/exchangeRate/USDRv', 'PATCH')) # ('/currencies/{code}', {'code': ''})


