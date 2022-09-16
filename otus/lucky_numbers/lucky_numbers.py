def lucky_numbers_junior():
    """
    Итеративный способ
    """
    count = 0
    for n1 in range(10):
        for n2 in range(10):
            for n3 in range(10):
                first3nums_sum = n1 + n2 + n3

                for n4 in range(10):
                    for n5 in range(10):
                        n6 = first3nums_sum - n4 - n5
                        if n6 >= 0 and n6 <= 9:
                            count += 1


class LuckyNumbersMiddle:
    """
    Рекурсивный способ
    """

    def __init__(self):
        self.count = 0

    def lucky_numbers(self, n, sum_a, sum_b):
        if n == 0:
            if sum_a == sum_b:
                self.count += 1
            return

        for a in range(10):
            for b in range(10):
                self.lucky_numbers(n - 1, sum_a + a, sum_b + b)


def lucky_numbers_middle_plus(amount_half_tickets):
    "Использование возможного варианта сумм"
    possible_sum_of_numbers = {
        key: 0 for key in range(9 * amount_half_tickets + 1)
    }
    possible_numbers = int(str(1).ljust(amount_half_tickets + 1, "0"))

    for possible_number in range(possible_numbers):
        num = sum(int(n) for n in [sn for sn in str(possible_number)])
        possible_sum_of_numbers[num] += 1

    return sum(
        number_count**2 for number_count in possible_sum_of_numbers.values()
    )


if __name__ == "__main__":
    from otus.test_service import TestService
    import os

    tests_path = os.path.join(os.getcwd(), "lucky_numbers", "test")
    service = TestService(lucky_numbers_middle_plus, tests_path)
    service.run_tests()
