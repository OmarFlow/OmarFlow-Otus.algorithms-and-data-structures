from typing import List


class CountingSort:
    """
    Сортировка подсчётом.

    Сложность - n. Стабильный. Не адаптивный. Не онлайн.
    """

    def __init__(self, array: List):
        self.array: List = array
        self.help_dict: dict = self.gen_help_dict()
        self.result_array = [None for _ in range(len(self.array))]

    def gen_help_dict(self) -> dict:
        """
        Создание дикта, где ключ - число, значение - кол-во его появлений в массиве.

        Значения суммируются.
        """
        _dict = dict()
        _dict = {key: 0 for key in set(self.array)}

        for i in self.array:
            _dict[i] += 1

        _value = None
        for key, value in _dict.items():
            if _value is None:
                _value = value
                continue
            _dict[key] += _value
            _value = _dict[key]

        return _dict

    def sorting(self) -> None:
        """
        Сортировка
        """
        for i in range(len(self.array) - 1, -1, -1):
            item = self.array[i]
            self.help_dict[item] -= 1

            index = self.help_dict[item]
            self.result_array[index] = item
