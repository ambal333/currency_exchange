import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection():
    connect = sqlite3.connect('currencies.db')
    try:
        yield connect
    finally:
        connect.close()

@contextmanager
def get_cursor(conn):
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()
