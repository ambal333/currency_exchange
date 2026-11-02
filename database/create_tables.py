import sqlite3

def init_database():
    connection = sqlite3.connect('currencies.db')
    cur = connection.cursor()

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
    connection.commit()
    connection.close()
    print('database is create')