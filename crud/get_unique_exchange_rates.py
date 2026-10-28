from database.db_connection import get_db_connection, get_cursor
from crud.format_data import format_exchange_rates
def get_unique_exchange_rates(code_1, code_2):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('SELECT er.id, bc.id, bc.fullname, '
                        'bc.code, bc.sign, tc.id, tc.fullname, '
                        'tc.code, tc.sign, er.rate FROM ExchangeRates as er '
                        'JOIN Currencies as bc ON er.basecurrencyid = bc.id '
                        'JOIN Currencies as tc ON er.targetcurrencyid = tc.id WHERE (bc.code, tc.code) = (?, ?);', (code_1, code_2))
            data = format_exchange_rates(cur.fetchall())
            # data = cur.fetchone()
            return data
