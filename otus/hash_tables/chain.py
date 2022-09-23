from dataclasses import dataclass
from typing import Hashable, Any, Optional, List, Generator

from otus.hash_tables.utils import check_key_hashable, KeyDoesNotExist

THRESHOLD_FACTOR = 0.5


@dataclass
class HashTableChainEntry:
    """
    Элемент хэш-таблицы
    """
    key: Hashable
    value: Any
    next_entry: Optional['HashTableChainEntry'] = None

    def is_key_equals(self, key: Hashable) -> bool:
        return self.key == key


class HashTableChain:
    """
    Хэш-таблица, использующая метод цепочек
    """

    table_size: int = 10000
    threshold: float = table_size * THRESHOLD_FACTOR
    size: int = 0

    def __init__(self):
        self.array: List[Optional[HashTableChainEntry]] = self.create_array()

    @check_key_hashable
    def __getitem__(self, key: Hashable) -> Any:
        first_entry_in_bucket: Optional[HashTableChainEntry] = self.get_first_entry_in_bucket(
            key)
        entry: HashTableChainEntry = HashTableChain.find_key_in_bucket(
            first_entry_in_bucket, key)
        return entry.value

    @check_key_hashable
    def __setitem__(self, key: Hashable, value: Any) -> None:
        first_entry_in_bucket: Optional[HashTableChainEntry] = self.get_first_entry_in_bucket(
            key)
        idx: int = HashTableChain.hash(key)

        # если ключ уже существует, меняем значение
        try:
            entry: HashTableChainEntry = HashTableChain.find_key_in_bucket(
                first_entry_in_bucket, key)
            entry.value = value
            return
        except KeyDoesNotExist:
            # иначе создаём запись и добавляем в ведро
            self.rehash()
            new_entry: HashTableChainEntry = HashTableChainEntry(
                key, value, next_entry=first_entry_in_bucket if first_entry_in_bucket else None)
            self.array[idx] = new_entry
            HashTableChain.size += 1
            return

    @check_key_hashable
    def remove(self, key: Hashable) -> None:
        """
        Удаление записи
        """
        first_entry_in_bucket: Optional[HashTableChainEntry] = self.get_first_entry_in_bucket(
            key)
        # собираем массив из ведра, для удобства удаления
        bucket: List[HashTableChainEntry] = [
            e for e in HashTableChain.bucket_generator(first_entry_in_bucket)]
        idx: int = HashTableChain.hash(key)

        if not bucket:
            raise KeyDoesNotExist

        if len(bucket) == 1 and bucket[0].is_key_equals(key):
            self.array[idx] = None
            HashTableChain.size -= 1
            return

        if bucket[0].is_key_equals(key):
            self.array[idx] = bucket[1]
            HashTableChain.size -= 1
            return

        if bucket[-1].is_key_equals(key):
            bucket[-2].next_entry = None
            HashTableChain.size -= 1
            return

        for entry in bucket[1:-1]:
            if entry.is_key_equals(key):
                bucket_idx: int = bucket.index(entry, 1, -1)
                bucket[bucket_idx - 1].next_entry = bucket[bucket_idx + 1]
                HashTableChain.size -= 1
                return

        raise KeyDoesNotExist

    def rehash(self) -> None:
        """
        Основной метод рехэширования
        """
        if HashTableChain.size > HashTableChain.threshold:
            # если величина таблицы больше допустимого значения - рехэшируем
            self.do_rehash()
        return

    @staticmethod
    def get_hash_code(key: Hashable) -> int:
        """
        Получение хэш кода
        """
        return abs(sum(ord(i) for i in str(key)))

    @staticmethod
    def hash(key: Hashable) -> int:
        """
        Получение хэша
        """
        hash_code: int = HashTableChain.get_hash_code(key)
        return hash_code % HashTableChain.table_size

    @staticmethod
    def bucket_generator(first_entry_in_bucket: Optional[HashTableChainEntry]) \
            -> Generator[HashTableChainEntry, None, None]:
        """
        Генератор ведра
        """
        entry = first_entry_in_bucket
        while entry:
            yield entry
            entry = entry.next_entry

    @staticmethod
    def find_key_in_bucket(first_entry_in_bucket: Optional[HashTableChainEntry], key: Hashable) -> HashTableChainEntry:
        """
        Возвращает запись, если ключ найден, иначе выкидывается исключение
        """
        for entry in HashTableChain.bucket_generator(first_entry_in_bucket):
            if entry.is_key_equals(key):
                return entry
        raise KeyDoesNotExist

    @classmethod
    def change_size_and_threshold(cls) -> None:
        cls.size = 0
        cls.table_size *= 2
        cls.threshold = cls.table_size * THRESHOLD_FACTOR

    def do_rehash(self) -> None:
        """
        Рехэширование
        """
        self.__class__.change_size_and_threshold()
        old_array: List[Optional[HashTableChainEntry]] = self.array
        self.array = self.create_array()  # type: ignore

        for bucket in old_array:
            entry = bucket
            while entry:
                self[entry.key] = entry.value
                entry = entry.next_entry

    def get_first_entry_in_bucket(self, key: Hashable) -> Optional[HashTableChainEntry]:
        """
        Получение первой записи ведра
        """
        idx: int = HashTableChain.hash(key)
        first_entry: Optional[HashTableChainEntry] = self.array[idx]
        return first_entry

    def create_array(self) -> List[None]:
        """
        Создание массива указанного в table_size размера
        """
        return [None for _ in range(HashTableChain.table_size)]
