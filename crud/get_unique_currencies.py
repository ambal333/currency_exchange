from database.db_connection import get_db_connection,get_cursor
from crud.format_data import format_currency
def get_unique_curren(code):
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM Currencies WHERE code = ?", (code,))
            data = format_currency(cur.fetchall())
    return data