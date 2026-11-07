import sqlite3


class DatabaseConnection:
    db_name = 'currencies.db'
    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()