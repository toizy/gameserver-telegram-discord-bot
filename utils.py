"""
    Модуль с утилитарными функциями
"""
from config import SMT_MIN, SMT_MAX


def clean_string_for_server(input_string):
    """
    Функция очищает строку от непечатных символов
    :param input_string: Оригинальная строка
    :return: Очищенная строка
    """
    result = ''
    for char in input_string:
        if char.isprintable():
            result += char
    return result


def check_server_message_type(value):
    """
    Функция проверяет тип серверного сообщения (SMT_*) на допустимое значение
    :param value: Тип сообщения
    :return: True - если тип в границах допустимого диапазона, False - если нет
    """
    return SMT_MIN <= value <= SMT_MAX
