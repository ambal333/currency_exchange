from database.db_connection import get_db_connection,get_cursor

def get_unique_curren(code):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM Currencies WHERE code = ?", (code,))
            data = cur.fetchone()
    if not data:
        return f'валюты {code} нет'
    return data