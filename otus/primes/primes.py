from math import sqrt


class IterativePrimes:
    """
    Итеративный способ
    """

    def count_primes(self, num: int) -> int:
        count = 0
        for i in range(2, num + 1):
            if self.is_prime(i):
                count += 1
        return count

    def is_prime(self, num: int) -> int:
        if num == 2:
            return True

        if num % 2 == 0:
            return False

        for i in range(3, round(sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True


class DivisionByPrimes:
    "С помощью деления на простые числа"

    def __init__(self):
        self.primes = [2]

    def count_primes(self, num: int) -> int:
        if num == 1:
            return 0

        count = 1
        for i in range(3, num + 1):
            if self.is_prime(i):
                count += 1
                self.primes.append(i)
        self.primes = [2]

        return count

    def is_prime(self, num: int):
        for i in self.primes:
            if num % i == 0:
                return False
        return True


if __name__ == "__main__":
    from otus.test_service import TestService
    import os

    pr = DivisionByPrimes()
    tests_path = os.path.join(os.getcwd(), "test")
    service = TestService(pr.count_primes, tests_path)
    service.run_tests()
