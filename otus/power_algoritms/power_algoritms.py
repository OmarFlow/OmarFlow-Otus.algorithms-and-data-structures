from math import log2, floor


def iterative_power(number: int, exponent: int) -> int:
    """
    Итеративный способ
    """
    result = 1
    for exp in range(1, exponent + 1):
        result *= number
    return result


def exponent_break_power(number: int, exponent: int) -> int:
    "C помощью разбивки степени"
    if exponent == 0:
        return 1
    exp = floor(log2(exponent))

    value = number
    for _ in range(exp):
        value *= value

    diff = exponent - 2**exp

    if diff != 0:
        for _ in range(diff):
            value *= number
    return value


def exponent_binary_break_power(number: int, exponent: int) -> int:
    """
    C помощью бинарной разбивки степени
    """
    exp = exponent
    value = number
    result = 1

    while exponent > 1:
        exponent //= 2
        value *= value
        if exponent % 2 == 1:
            result *= value

    if exp % 2 == 1:
        result *= number

    return result


if __name__ == "__main__":
    from otus.test_service import TestService
    import os

    tests_path = os.path.join(os.getcwd(), "test")
    service = TestService(iterative_power, tests_path)
    service.run_tests()
