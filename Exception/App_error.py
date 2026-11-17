class AppError(Exception):
    def __init__(self, status_code, message):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __str__(self):
        return self.message


class CodeStandardError(AppError):
    pass


class CurrExchangeNotExist(AppError):
    pass


class CurrencyNotFound(AppError):
    pass


class ExchangeRateNotFound(AppError):
    pass


class ExchangeRateCodeNotFound(AppError):
    pass


class NameStandardError(AppError):
    pass


class FormFieldError(AppError):
    pass


class IntegrityError(AppError):
    pass


class DatabaseError(AppError):
    pass


class CodeNotFoundError(AppError):
    pass


class NotExistExchangeRate(AppError):
    pass


class RateValidError(AppError):
    pass


class IntegrityExchangeError(AppError):
    pass


class FormatFormError(AppError):
    pass


class CourseNotExist(AppError):
    pass


class AmountLessZero(AppError):
    pass