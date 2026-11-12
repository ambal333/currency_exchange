from DAO.base_dao import BaseDao


class CurrenciesDao(BaseDao):
    """Используется для получения и добавления валют в базу данных

    Методы
    ------
    get_all_currencies
        получение всех валют из бд
    get_unique_currency
        получение конкретной валюты по коду
    insert_currency
        добавление новой валюты в бд
    """

    def get_all_currencies(self) -> list[tuple]:
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT id, fullname, code, sign FROM Currencies")
            return cur.fetchall()
        finally:
            cur.close()

    def get_unique_currency(self, code: str) -> tuple:
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT * FROM Currencies WHERE code = ?", (code,))
            return cur.fetchone()
        finally:
            cur.close()

    def insert_currency(self, code: str, fullname: str, sign: str) -> tuple:
        cur = self.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO Currencies(code, fullname, sign) VALUES (?,?,?)",
                (code, fullname, sign)
                )
            self.connection.commit()

            cur.execute('SELECT id, fullname, code, sign FROM Currencies '
                        'WHERE code = ?',
                        (code,)
                        )
            data = cur.fetchone()
            return data
        finally:
            cur.close()





