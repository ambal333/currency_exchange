import sqlite3

from database.db_connection import DatabaseConnection

class BaseDao:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def get_currency_id_by_code(self, code):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT id FROM Currencies WHERE code = ?', (code,))
            return cur.fetchone()
        except sqlite3.Error:
            raise
        finally:
            cur.close()