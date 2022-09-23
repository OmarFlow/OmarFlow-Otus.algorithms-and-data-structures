from math import sqrt, floor
from decimal import Decimal


def iterative_fibonacci(num: int) -> int:
    """
    Итеративный способ
    """
    if num < 2:
        return num

    if num == 2:
        return 1

    a = 1
    b = 1

    for i in range(3, num + 1):
        f = a + b
        a = b
        b = f

    return f


def recursive_fibonacci(num: int) -> int:
    """
    Рекурсивный способ
    """
    if num <= 1:
        return num
    return recursive_fibonacci(num - 1) + recursive_fibonacci(num - 2)


def golden_fibonacci(num: int) -> int:
    """
    Использование золотого сечения
    """
    f = Decimal((1 + sqrt(5)) / 2)
    fib = floor(f**num / Decimal(sqrt(5)) + Decimal(0.5))
    return fib


if __name__ == "__main__":
    from otus.test_service import TestService
    import os

    tests_path = os.path.join(os.getcwd(), "test")
    service = TestService(golden_fibonacci, tests_path)
    service.run_tests()
