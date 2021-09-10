"""

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: As 1! = 1 and 2! = 2 are not sums they are not included.

"""
import math
import operator
from bisect import bisect_left
from typing import Iterator

FACTORIALS = [math.factorial(i) for i in range(10)]


def digits(n: int) -> Iterator[int]:
    """Iterate over digits of n from least significant to most significant digit."""
    yield n % 10
    n //= 10
    while n:
        yield n % 10
        n //= 10


def check(n, condition):
    """Check number against sum of digits factorial."""
    digit_factorial_sum = sum(FACTORIALS[d] for d in digits(n))
    return condition(digit_factorial_sum, n)


def max_n_as_factorial_sum():
    """Find the smallest number n which can not be represented as digits factorial sum."""
    k = 1
    n = 10
    while n <= k * FACTORIALS[9]:
        k += 1
        n *= 10
    return n


def project_euler_main():
    """Solution for Project Euler."""
    max_n = max_n_as_factorial_sum()
    print(max_n)
    numbers = [i for i in range(10, max_n) if check(i, operator.eq)]
    print(numbers, sum(numbers))


def hacker_rank_main():
    """Solution for hacker rank."""
    n = int(input())
    print(sum(i for i in range(10, n) if not check(i, operator.mod)))


# project_euler_main()
hacker_rank_main()




