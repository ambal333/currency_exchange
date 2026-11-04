import sqlite3
from typing import Union

from DAO.base_dao import BaseDao
from Exception.integrity_exchange_error import IntegrityExchangeError
from Exception.not_exist_exchange_rate import NotExistExchangeRate
from Exception.not_exist_in_db import NotExistInDb


class ExchangeRatesDao(BaseDao):

    def get_unique_exchange_rates(self, code_1: str, code_2: str):
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
            return cur.fetchall()
        finally:
            cur.close()

    def insert_exchange_rates(self, code_1: str, code_2: str, rate: Union[int, float]):
        cur = self.connection.cursor()
        try:
            id_1 = self.get_currency_id_by_code(code_1)
            id_2 = self.get_currency_id_by_code(code_2)
            print(id_1, id_2)
            if id_1 is not None and id_2 is not None:
                is_unique = self.get_unique_exchange_rates(code_1, code_2)
                if is_unique:
                    raise IntegrityExchangeError('Валютная пара с таким кодом уже существует')

                cur.execute('INSERT INTO ExchangeRates(basecurrencyid, '
                                'targetcurrencyid, rate) VALUES (?, ?, ?)',
                                (id_1[0], id_2[0], rate))
                self.connection.commit()
                data = self.get_unique_exchange_rates(code_1, code_2)
                return data
            else:
                raise NotExistInDb('Одна (или обе) валюта из валютной пары не существует в БД')
        finally:
            cur.close()

    def patch_exchange_rates(self, code_1: str, code_2: str, rate: Union[int, float]):
        cur = self.connection.cursor()
        try:
            exchange_rate = self.get_unique_exchange_rates(code_1, code_2)
            if exchange_rate:
                cur.execute('UPDATE ExchangeRates SET rate = ? WHERE '
                            'basecurrencyid = (SELECT id FROM Currencies WHERE code = ?) AND '
                            'targetcurrencyid = (SELECT id FROM Currencies WHERE code = ?)',
                            (rate, code_1, code_2))
                self.connection.commit()
            else:
                raise NotExistExchangeRate('Валютная пара отсутствует в базе данных')
        finally:
            cur.close()