from math import sqrt


class IterativePrimes:
    """
    Итеративный способ
    """
    def __init__(self, num):
        self.num = num

    def count_primes(self):
        count = 0
        for i in range(2, self.num+1):
            if self.is_prime(i):
                count += 1
        return count

    def is_prime(self, num):
        if num == 2:
            return True

        if num % 2 == 0:
            return False

        for i in range(3, round(sqrt(num))+1, 2):
            if num % i == 0:
                return False
        return True


class DivisionByPrimes:
    "С помощью деления на простые числа"
    def __init__(self, num):
        self.num = num
        self.primes = [2]

    def count_primes(self):
        count = 1
        for i in range(3, self.num+1):
            if self.is_prime(i):
                count += 1
                self.primes.append(i)
        return count

    def is_prime(self, num):
        for i in self.primes:
            if num % i == 0:
                return False
        return True

j = DivisionByPrimes(1000)
print(j.count_primes())
print(j.primes)