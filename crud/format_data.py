def format_currency(data):
    all_currency = []
    for i in data:
        all_currency.append({"id": i[0],
                             "code": i[1],
                             "name": i[2],
                             "sign": i[3]})
    print(all_currency)
    return all_currency

def format_exchange_rates(data):
    result = []
    for i in data:
        result.append(
            {
                "id": i[0],
                "baseCurrency": {
                    "id": i[1],
                    "name": i[2],
                    "code": i[3],
                    "sign": i[4]
                },
                "targetCurrency": {
                    "id": i[5],
                    "name": i[6],
                    "code": i[7],
                    "sign": i[8]
                },
                "rate": i[9]
            }
        )
    return result