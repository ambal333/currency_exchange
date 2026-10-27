from database.db_connection import get_db_connection, get_cursor
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
                    basecurrencyid INTEGER REFERENCES Currencies(ID),
                    targetcurrencyid INTEGER REFERENCES Currencies(ID),
                    rate NUMERIC(4,6) NOT NULL);
                ''')
            conn.commit()
    print('database is create')