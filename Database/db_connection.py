import os
import sqlite3

from dotenv import load_dotenv


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
    load_dotenv()
    db_name = os.getenv('DB_NAME')

    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()
