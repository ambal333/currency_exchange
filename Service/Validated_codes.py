from urllib.parse import unquote

from Exception.App_error import (IntegrityError,
                                 CodeStandardError,
                                 NameStandardError)


class CheckCodes:
    """Класс служит для проверки полей code и name

    Методы
    ______
    validated_cods
        валидация двух кодов для обменных курсов
    validated_code_name
        валидация code, name для валют
    """

    __LENGTH_CODE = 3

    @classmethod
    def validated_cods(cls, code_1: str, code_2: str) -> None:
        decode_code_1 = unquote(code_1)
        decode_code_2 = unquote(code_2)

        if decode_code_1 == decode_code_2:
            raise IntegrityError(
                400,
                'Валюты не должны совпадать.'
            )

        if (len(decode_code_1) != cls.__LENGTH_CODE or len(decode_code_2) !=
                cls.__LENGTH_CODE):
            raise CodeStandardError(
                400,
                'Оба кода должны состоять из 3 символов.'
            )

        if (decode_code_1 != decode_code_1.upper() or
                decode_code_2 != decode_code_2.upper()):
            raise CodeStandardError(
                400,
                'Коды должны быть в верхнем регистре.'
            )

        if not ((decode_code_1.isalpha() and decode_code_1.isascii()) and (
                decode_code_2.isalpha() and decode_code_2.isascii())):
            raise CodeStandardError(
                400,
                'Коды должны состоять из английских букв.'
            )

    @classmethod
    def validated_code_name(cls, code: str, name=None) -> None:
        decode_code = unquote(code)
        if len(decode_code) != cls.__LENGTH_CODE:
            raise CodeStandardError(
                400,
                'Код должен состоять из 3 символов.'
            )

        if decode_code != decode_code.upper():
            raise CodeStandardError(
                400,
                'Код должен быть в верхнем регистре.'
            )

        if not (decode_code.isalpha() and decode_code.isascii()):
            raise CodeStandardError(
                400,
                'Код должен состоять из английских букв.'
            )
        if name:
            decode_name = unquote(name)
            if not (decode_name.isascii()):
                raise NameStandardError(
                    400,
                    'Название валюты должно состоять из '
                    'английских символов.'
                )
