import sqlite3
from contextlib import contextmanager

class DatabaseConnection:
    db_name = 'currencies.db'
    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()
    # @contextmanager
    # def get_connect(self):
    #     connect = None
    #     try:
    #         connect = sqlite3.connect(self.db_name)
    #         yield connect
    #     except sqlite3.Error as error:
    #         print(f'Ошибка базы данных: {error}')
    #         raise
    #     finally:
    #         if connect:
    #             connect.close()

    # @contextmanager
    # def get_cursor(self):
    #     with self.get_db_connection() as conn:
    #         cur = conn.cursor()
    #         try:
    #             yield cur
    #         finally:
    #             cur.close()