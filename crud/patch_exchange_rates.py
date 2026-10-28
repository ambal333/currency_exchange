from database.db_connection import get_db_connection, get_cursor
from crud.get_unique_exchange_rates import get_unique_exchange_rates
def patch_exchange_rate(rate, code_1, code_2):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('UPDATE ExchangeRates SET rate = ? WHERE '
                        'basecurrencyid = (SELECT id FROM Currencies WHERE code = ?) AND '
                        'targetcurrencyid = (SELECT id FROM Currencies WHERE code = ?)', (rate, code_1, code_2))
            conn.commit()
            data = get_unique_exchange_rates(code_1, code_2)
            return data