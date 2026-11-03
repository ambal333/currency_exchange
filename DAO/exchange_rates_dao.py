import sqlite3
from typing import Union

from DAO.base_dao import BaseDao

class ExchangeRatesDao(BaseDao):

    def get_unique_exchange_rates(self, code_1, code_2):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT er.id, bc.id, bc.fullname, '
                        'bc.code, bc.sign, tc.id, tc.fullname, '
                        'tc.code, tc.sign, er.rate FROM ExchangeRates as er '
                        'JOIN Currencies as bc ON er.basecurrencyid = bc.id '
                        'JOIN Currencies as tc ON er.targetcurrencyid = tc.id WHERE (bc.code, tc.code) = (?, ?);',
                        (code_1, code_2))
            return cur.fetchone()
        finally:
            cur.close()

    def get_exchange_rates(self):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT er.id, bc.id, bc.fullname, '
                        'bc.code, bc.sign, tc.id, tc.fullname, '
                        'tc.code, tc.sign, er.rate FROM ExchangeRates as er '
                        'JOIN Currencies as bc ON er.basecurrencyid = bc.id '
                        'JOIN Currencies as tc ON er.targetcurrencyid = tc.id;')
            return cur.fetchone()
        finally:
            cur.close()

    def insert_exchange_rates(self, code_1: str, code_2: str, rate: Union[int, float]):
        cur = self.connection.cursor()
        try:
            id_1 = self.get_currency_id_by_code(code_1)
            id_2 = self.get_currency_id_by_code(code_2)
            cur.execute('INSERT INTO ExchangeRates(basecurrencyid, '
                        'targetcurrencyid, rate) VALUES (?, ?, ?)',(id_1, id_2, rate))
            self.connection.commit()
            data = self.get_unique_exchange_rates(code_1, code_2)
            return data
        except sqlite3.Error:
            raise
        finally:
            cur.close()

    def patch_exchange_rates(self, code_1: str, code_2: str, rate: Union[int, float]):
        cur = self.connection.cursor()
        try:
            cur.execute('UPDATE ExchangeRates SET rate = ? WHERE '
                        'basecurrencyid = (SELECT id FROM Currencies WHERE code = ?) AND '
                        'targetcurrencyid = (SELECT id FROM Currencies WHERE code = ?)',
                        (rate, code_1, code_2))
            self.connection.commit()
        except sqlite3.Error:
            raise
        finally:
            cur.close()