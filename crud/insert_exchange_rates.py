from database.db_connection import get_db_connection, get_cursor
from crud.format_data import format_exchange_rates, format_currency
from crud.get_unique_exchange_rates import get_unique_exchange_rates
def insert_exchange_rate(code_1, code_2, rate):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            print(f'base:{code_1}')
            cur.execute('SELECT id FROM Currencies WHERE code = ? OR code = ?', (code_1, code_2))
            currencies = cur.fetchall()
            print(currencies)
            if len(currencies) < 2:
                return 404, {'error': 'Одна (или обе) валюта из валютной пары не существует в БД'}
            # id_currency_1, id_currency_2 = currencies
            cur.execute('SELECT id FROM Currencies WHERE code = ?', (code_1,))
            id_currency_1 = cur.fetchone()
            cur.execute('SELECT id FROM Currencies WHERE code = ?', (code_2,))
            id_currency_2 = cur.fetchone()
            print(id_currency_1, id_currency_2)
            cur.execute('SELECT * FROM ExchangeRates WHERE basecurrencyid = ? AND targetcurrencyid = ?', (id_currency_1[0], id_currency_2[0]))
            select_exchange = cur.fetchone()
            print(select_exchange)
            if select_exchange:
                return 409, {'error': 'Валютная пара с таким кодом уже существует'}
            cur.execute('INSERT INTO ExchangeRates(basecurrencyid, targetcurrencyid, rate) VALUES (?, ?, ?)', (id_currency_1[0], id_currency_2[0], rate))
            conn.commit()
            # cur.execute('SELECT * FROM ExchangeRates WHERE basecurrencyid = ? AND targetcurrencyid = ?', (id_currency_1[0], id_currency_2[0]))
            exchange = get_unique_exchange_rates(code_1, code_2)
            return 201, exchange

