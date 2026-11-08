import sqlite3


class DatabaseConnection:
    """ Используется для подключения к базе данных.

    Атрибуты
    --------
    connection
        соединение с базой данных

    Методы
    ------
    close
        отвечает за закрытие подключения к базе данных
    """
    db_name = 'currencies.db'

    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()
