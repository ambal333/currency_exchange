
from database.db_connection import get_db_connection, get_cursor
# with sqlite3.connect('currencies.db') as connection:
#     cursor = connection.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS Currencies(
#         id INTEGER PRIMARY KEY,
#         code VARCHAR UNIQUE NOT NULL,
#         fullname VARCHAR NOT NULL,
#         sign VARCHAR NOT NULL
#         )
#     ''')

def init_database():
    with get_db_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS Currencies(
                    id INTEGER PRIMARY KEY,
                    code VARCHAR(40) NOT NULL UNIQUE,
                    fullname VARCHAR(64) NOT NULL,
                    sign VARCHAR(10) NOT NULL);
                ''')
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS ExchangeRates(
                    id INTEGER PRIMARY KEY,
                    basecurrencyid INTEGER REFERENCES Currencies(ID) UNIQUE,
                    targetcurrencyid INTEGER REFERENCES Currencies(ID) UNIQUE,
                    rate NUMERIC(4,6) NOT NULL);
                ''')
            conn.commit()
    print('database is create')

