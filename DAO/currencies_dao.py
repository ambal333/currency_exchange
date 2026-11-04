import sqlite3

from DAO.base_dao import BaseDao

class CurrenciesDao(BaseDao):

    def get_all_currencies(self):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT * FROM Currencies")
            return cur.fetchall()
        finally:
            cur.close()

    def get_unique_currency(self, code):
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT * FROM Currencies WHERE code = ?", (code,))
            return cur.fetchone()
        finally:
            cur.close()

    def insert_currency(self, code, fullname, sign):
        cur = self.connection.cursor()
        try:
            cur.execute(
                f"INSERT INTO Currencies(code, fullname, sign) VALUES (?,?,?)",
                (code, fullname, sign))
            self.connection.commit()
        finally:
            cur.close()
# init_database()
# conn = sqlite3.connect('currencies.db')
#
# currencies = CurrenciesDao(conn)
# currencies.insert_currency('EUR', 'Euro', '%')
# print(currencies.get_all_currencies())
#
# conn.close





