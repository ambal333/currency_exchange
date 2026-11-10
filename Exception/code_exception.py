class CodeNotFoundError(Exception):
    """Используется для отображения ошибки - отсутствия кода валюты в адресе
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

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
