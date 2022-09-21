from typing import Callable, Hashable
from functools import wraps


def check_key_hashable(func: Callable) -> Callable:
    """
    Проверка хэшируемости ключа
    """
    @wraps(func)
    def wr(*args: tuple) -> Callable:
        key: Hashable = args[1]
        if not isinstance(key, Hashable):
            raise Exception("key must be hashable")
        elif key is None:
            raise Exception("None not permitted as key")
        return func(*args)
    return wr


class KeyDoesNotExist(Exception):
    """
    Выкидывается, если ключа нет в таблице
    """

    def __init__(self):
        super().__init__(*("the key does not exist",))


class HashTableDeletedItem:
    """
    Заглушка удалённого элемента хэш-таблицы
    """
