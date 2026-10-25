import sqlite3

from database.db_connection import get_db_connection,get_cursor

def insert_currency(code, fullname, sign):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('SELECT fullname FROM Currencies WHERE code = ?', (code, ))
            get_currency = cur.fetchone()
            if get_currency:
                return 409, {'error': f'валюта {code} уже существует'}
            else:
                cur.execute(f"INSERT INTO Currencies(code, fullname, sign) VALUES (?,?,?)", (code, fullname, sign))
                conn.commit()
            cur.execute('SELECT * FROM Currencies WHERE code = ?', (code, ))
            created_currency = cur.fetchone()
    return 201, created_currency
