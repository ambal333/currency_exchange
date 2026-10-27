from database.db_connection import get_db_connection, get_cursor
from crud.format_data import format_currency
def insert_exchange_rate(basecurrencyid, targetcurrencyid, rate):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('SELECT * FROM ExchangeRates WHERE basecurrencyid = ? AND targetcurrencyid = ?', (basecurrencyid, targetcurrencyid))
            select_exchange = cur.fetchone()
            if select_exchange:
                return 409, {'error': 'Валютная пара с таким кодом уже существует'}
            cur.execute('INSERT INTO ExchangeRates(basecurrencyid, targetcurrencyid, rate) VALUES (?, ?, ?)', (basecurrencyid, targetcurrencyid, rate))
            cur.execute('SELECT * FROM ExchangeRates WHERE basecurrencyid = ? AND targetcurrencyid = ?', (basecurrencyid, targetcurrencyid))
            exchange = cur.fetchall()
            conn.commit()
            return 201, exchange

