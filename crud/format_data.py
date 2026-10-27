def format_currency(data):
    all_currency = []
    for i in data:
        all_currency.append({"id": i[0],
                             "code": i[1],
                             "name": i[2],
                             "sign": i[3]})
    print(all_currency)
    return all_currency