class CountingSort:
    def __init__(self, array):
        self.array = array
        self.help_dict = self.gen_help_dict()
        self.result_array = [None for _ in range(len(self.array))]

    def gen_help_dict(self):
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

    def sorting(self):
        for i in range(len(self.array) - 1, -1, -1):
            item = self.array[i]
            self.help_dict[item] -= 1

            index = self.help_dict[item]
            self.result_array[index] = item


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer
    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]
    f = [randint(1, 1000000) for _ in range(1000000000)]

    for i in a, b, c, d, e:
        ss = CountingSort(i)
        start = timer()
        ss.sorting()
        end = timer()
        print(end - start)