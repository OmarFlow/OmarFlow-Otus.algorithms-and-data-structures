from dataclasses import dataclass
from functools import wraps
from typing import Hashable, Any, Optional, List, Callable, Generator

THRESHOLD_FACTOR = 0.75


class KeyDoesNotExist(Exception):
    """
    Выкидывается, когда ключа нет в таблице
    """

    def __init__(self):
        super().__init__(*("the key does not exist",))


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


@dataclass
class HashTableEntry:
    """
    Элемент хэш-таблицы
    """
    key: Hashable
    value: Any
    next_entry: Optional['HashTableEntry'] = None

    def is_key_equals(self, key: Hashable) -> bool:
        return self.key == key


class HashTableChain:
    """
    Хэш-таблица, использующая метод цепочек
    """

    table_size: int = 1
    threshold: float = table_size * THRESHOLD_FACTOR
    size: int = 0

    def __init__(self):
        self.array: List[Optional[HashTableEntry]] = self.create_array()

    @check_key_hashable
    def __getitem__(self, key: Hashable) -> Any:
        first_entry_in_bucket: Optional[HashTableEntry] = self.get_first_entry_in_bucket(
            key)
        entry: HashTableEntry = HashTableChain.find_key_in_bucket(
            first_entry_in_bucket, key)
        return entry.value

    @check_key_hashable
    def __setitem__(self, key: Hashable, value: Any) -> None:
        first_entry_in_bucket: Optional[HashTableEntry] = self.get_first_entry_in_bucket(
            key)
        idx: int = HashTableChain.hash(key)

        # если ключ уже существует, меняем значение
        try:
            entry: HashTableEntry = HashTableChain.find_key_in_bucket(
                first_entry_in_bucket, key)
            entry.value = value
            return
        except KeyDoesNotExist:
            # иначе создаём запись и добавляем в ведро
            self.rehash()
            new_entry: HashTableEntry = HashTableEntry(
                key, value, next_entry=first_entry_in_bucket if first_entry_in_bucket else None)
            self.array[idx] = new_entry
            HashTableChain.size += 1
            return

    @check_key_hashable
    def remove(self, key: Hashable) -> None:
        """
        Удаление записи
        """
        first_entry_in_bucket: Optional[HashTableEntry] = self.get_first_entry_in_bucket(
            key)
        # собираем массив из ведра, для удобства удаления
        bucket: List[HashTableEntry] = [
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
    def bucket_generator(first_entry_in_bucket: Optional[HashTableEntry]) -> Generator[HashTableEntry, None, None]:
        """
        Генератор ведра
        """
        entry = first_entry_in_bucket
        while entry:
            yield entry
            entry = entry.next_entry

    @staticmethod
    def find_key_in_bucket(first_entry_in_bucket: Optional[HashTableEntry], key: Hashable) -> HashTableEntry:
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
        old_array: List[Optional[HashTableEntry]] = self.array
        self.array = self.create_array()  # type: ignore

        for bucket in old_array:
            entry = bucket
            while entry:
                self[entry.key] = entry.value
                entry = entry.next_entry

    def get_first_entry_in_bucket(self, key: Hashable) -> Optional[HashTableEntry]:
        """
        Получение первой записи ведра
        """
        idx: int = HashTableChain.hash(key)
        first_entry: Optional[HashTableEntry] = self.array[idx]
        return first_entry

    def create_array(self) -> List[None]:
        """
        Создание массива указанного в table_size размера
        """
        return [None for _ in range(HashTableChain.table_size)]
