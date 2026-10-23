def format_currency(data):
    all_currency = []
    # dict_data = {"id": None,
    #     "name": None,
    #     "code": None,
    #     "sign": None}
    for i in data:
        all_currency.append({"id": i[0],
                             "code": i[1],
                             "name": i[2],
                             "sign": i[3]})
    return all_currency