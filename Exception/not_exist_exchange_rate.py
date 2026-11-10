class NotExistExchangeRate(Exception):
    """Используется для отображения ошибки - валютная пара отсутствует в
    базе данных
    запроса

    Атрибуты
    --------
    message
        текст возникающего исключения
    Методы
    ------
    __str__
        магический метод для отображения message
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
