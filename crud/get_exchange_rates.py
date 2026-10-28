from database.db_connection import get_db_connection, get_cursor
from crud.format_data import format_exchange_rates
def get_exchange_rates():
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('SELECT er.id, bc.id, bc.fullname, '
                        'bc.code, bc.sign, tc.id, tc.fullname, '
                        'tc.code, tc.sign, er.rate FROM ExchangeRates as er '
                        'JOIN Currencies as bc ON er.basecurrencyid = bc.id '
                        'JOIN Currencies as tc ON er.targetcurrencyid = tc.id;')
            # cur.execute('SELECT * FROM ExchangeRates')
            data = format_exchange_rates(cur.fetchall())
            return data


# [
#     {
#         "id": 0,
#         "baseCurrency": {
#             "id": 0,
#             "name": "United States dollar",
#             "code": "USD",
#             "sign": "$"
#         },
#         "targetCurrency": {
#             "id": 1,
#             "name": "Euro",
#             "code": "EUR",
#             "sign": "€"
#         },
#         "rate": 0.99
#     }
# ]


# CREATE TABLE IF NOT EXISTS ExchangeRates(
#                     id INTEGER PRIMARY KEY,
#                     basecurrencyid INTEGER REFERENCES Currencies(ID),
#                     targetcurrencyid INTEGER REFERENCES Currencies(ID),
#                     rate NUMERIC(4,6) NOT NULL);






