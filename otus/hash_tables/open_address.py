from dataclasses import dataclass
import random
from typing import Hashable, Any, Optional, List, Union

from otus.hash_tables.utils import check_key_hashable, KeyDoesNotExist, HashTableDeletedItem

THRESHOLD_FACTOR = 0.5


@dataclass
class HashTableOpenAddressEntry:
    """
    Элемент хэш-таблицы
    """
    key: Hashable
    value: Any

    def is_key_equals(self, key: Hashable) -> bool:
        return self.key == key


class HashTableOpenAddress:
    """
    Хэш-таблица, реализованная методом открытой адресации
    """

    table_size: int = 50000
    table_size_for_hash: int = table_size - 1
    threshold: float = table_size * THRESHOLD_FACTOR
    size: int = 0
    table: List[int] = [i for i in range(256)]
    random.shuffle(table)

    def __init__(self):
        self.array: List[Optional[HashTableOpenAddressEntry]
                         ] = self.create_array()

    @check_key_hashable
    def __getitem__(self, key: Hashable) -> Any:
        probing: int = 1
        while True:
            entry, idx = self.get_entry(key, probing)
            if entry is None or isinstance(entry, HashTableDeletedItem):
                raise KeyDoesNotExist()
            if entry.is_key_equals(key):
                return entry.value
            probing += 1
            continue

    @check_key_hashable
    def __setitem__(self, key: Hashable, value: Any) -> None:
        probing: int = 1
        while True:
            entry, idx = self.get_entry(key, probing)
            if entry is None or isinstance(entry, HashTableDeletedItem):
                self.array[idx] = HashTableOpenAddressEntry(key, value)
                HashTableOpenAddress.size += 1
                self.rehash()
                return
            elif entry.key == key:
                self.array[idx].value = value
                return
            probing += 1
            continue

    @check_key_hashable
    def remove(self, key: Hashable) -> None:
        """
        Удаление записи
        """
        probbing: int = 1
        while True:
            entry, idx = self.get_entry(key, probbing)
            if entry is None or isinstance(entry, HashTableDeletedItem):
                raise KeyDoesNotExist()
            elif entry.key != key:
                probbing += 1
                continue
            else:
                self.array[idx] = HashTableDeletedItem()  # type: ignore
                return

    @staticmethod
    def get_hash_code(key: Hashable) -> int:
        """
        Получение хэш кода
        """
        hh = []
        for i in range(7):
            h = HashTableOpenAddress.table[(
                ord(key[0]) + i) % 256]  # type: ignore
            for letter in str(key):
                h = HashTableOpenAddress.table[h ^ ord(letter)]
            hh.append(h)
        return sum(hh)

    @staticmethod
    def hash(key: Hashable, probing_factor: int) -> int:
        """
        Получение хэша
        """
        hash_code: int = HashTableOpenAddress.get_hash_code(key)
        hash1: int = hash_code % HashTableOpenAddress.table_size
        hash2: int = (hash_code %
                      HashTableOpenAddress.table_size_for_hash) * probing_factor
        return (hash1 + hash2) % HashTableOpenAddress.table_size

    def get_entry(self, key: Hashable, probing_factor: int) -> tuple:
        """
        Получение записи в массиве
        """
        idx: int = HashTableOpenAddress.hash(key, probing_factor)
        entry: Union[HashTableOpenAddressEntry,
                     HashTableDeletedItem, None] = self.array[idx]
        return entry, idx

    def rehash(self) -> None:
        """
        Основной метод рехэширования
        """
        if HashTableOpenAddress.size > HashTableOpenAddress.threshold:
            # если величина таблицы больше допустимого значения - рехэшируем
            self.do_rehash()
        return

    def do_rehash(self) -> None:
        """
        Рехэширование
        """
        self.__class__.change_size_and_threshold()
        old_array: List[Optional[HashTableOpenAddressEntry]] = self.array
        self.array = self.create_array()  # type: ignore
        for entry in old_array:
            if isinstance(entry, HashTableOpenAddressEntry):
                self[entry.key] = entry.value
            continue

    @classmethod
    def change_size_and_threshold(cls) -> None:
        cls.size = 0
        cls.table_size *= 2
        cls.table_size_for_hash = cls.table_size - 1
        cls.threshold = cls.table_size * THRESHOLD_FACTOR

    def create_array(self) -> List[None]:
        """
        Создание массива указанного в table_size размера
        """
        return [None for _ in range(HashTableOpenAddress.table_size)]
