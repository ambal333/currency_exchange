from database.db_connection import DatabaseConnection


class BaseDao:
    """Базовый класс для всех DAO классов.

    Атрибуты
    --------
    connection: DatabaseConnection
        обеспечивает связь с бд

    Методы
    ------
    __create_tables
        создает таблицы в бд и добавляет несколько валют
    get_currency_id_by_code
        осуществляет получение ID валюты по конкретному коду
    """

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
        self.__create_tables()

    def __create_tables(self):
        cur = self.connection.cursor()
        try:
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
                            rate DECIMAL(6) NOT NULL);
                        ''')
            self.connection.commit()

            cur.execute('SELECT COUNT(id) FROM Currencies')
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Currencies(code, fullname, sign) "
                    "VALUES (?,?,?)",
                    ('EUR', 'Euro', '€'))
                cur.execute(
                    "INSERT INTO Currencies(code, fullname, sign) "
                    "VALUES (?,?,?)",
                    ('USD', 'United States dollar', '$'))
                cur.execute(
                    "INSERT INTO Currencies(code, fullname, sign) "
                    "VALUES (?,?,?)",
                    ('RUB', 'Russian rubles', '₽'))
                self.connection.commit()
        finally:
            cur.close()

    def get_currency_id_by_code(self, code: str) -> tuple:
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT id FROM Currencies WHERE code = ?', (code,))
            return cur.fetchone()
        finally:
            cur.close()