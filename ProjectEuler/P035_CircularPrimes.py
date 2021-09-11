"""

The number, 197, is called a circular prime because all rotations of the digits:
    197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
Find the sum of circular primes that are below N?

"""
import itertools
import math
from functools import reduce
from typing import Iterator, Iterable


def divisors(num: int, *, start: int = 2, ordered: bool = False, step: int = 1) -> Iterator[int]:
    """
    Get all number divisors starting from start.
    Faster (sqrt(n) operations) than scanning all numbers using:
        divisors = (i for i in range(start, n) if n % mod i == 0).
    :param step: step for verifying sequence of divisors (1= all numbers, 2 - odd numbers)
    :param num: number for which we yields divisors
    :param ordered: if True divisors yields in increasing order
        using list keeping half of the divisors.
        For ordered=True risk of memory overflow for huge numbers with few thousands digits
    :param start: starting number for divisor.
        Most frequent use:
            start=2 yields all divisors excluding 1 and n -  it will contains nothing for prime num
            start=1 yields all divisors including 1 and n -  it will contain 1 and num for prime num
            start is used for step by step number factorization
            (finding number representation as prime number product)
    :yields: num divisors
    """

    def _divisors():
        # Step 1:
        # Process divisible by 1 only when start == 1
        if start == 1:
            yield 1
            # prevent yield duplicate when num == 1
            if num > 1:
                yield num

        # Step 2:
        # Process divisibility in up to sqrt_num[+1]
        # - from 2 (1 already processed) or from start if greater then 2
        # - to sqrt_num if sqrt_num is exact square of num or once more otherwise
        for next_num in range(max(2, start), sqrt_num + no_int_sqrt, step):
            if num % next_num == 0:
                yield next_num
                yield num // next_num

        # Step 3:
        # Process when sqrt_num is exact sqrt of num except 1 which was already processed in step 1
        if no_int_sqrt == 0 and num > 1:
            yield sqrt_num

    def _sorted(iterable: Iterable[int]):
        # Divisor are not generated in sorted order. E.g. for 12 it is: 1, 12, 2, 6, 3, 4.
        # Odd elements are increasing, even elements are decreasing
        # Make stack for half of divisors if ordered list of divisors is requested
        divisors_stack: list[int] = []
        iterator = iter(iterable)

        try:
            previous = next(iterator)
        except StopIteration:
            return

        for current in iterator:
            if previous > current:
                # Send even element on stack
                divisors_stack.append(previous)
            else:
                # Yield odd element
                yield previous
            previous = current
        # Yield last ordered element
        yield previous

        # Yield elements from stack
        for divisor in reversed(divisors_stack):
            yield divisor

    assert num > 0, "divisors iterator works with num > 0"
    assert start > 0, "divisors iterator works with start > 0"

    # find divisors until sqrt(num)
    sqrt_num: int = int(math.sqrt(num))
    # Is exact num sqrt?
    if sqrt_num * sqrt_num == num:
        no_int_sqrt = 0
    else:
        no_int_sqrt = 1

    if ordered:
        yield from _sorted(_divisors())
    else:
        yield from _divisors()


def prime_divisors(num: int) -> Iterator[int]:
    """
    Get all num prime divisors.
    :param num: number for which we yields prime divisors
    :yields: num prime divisors
    """
    assert num > 0

    if num == 1:
        yield 1

    while num % 2 == 0:
        yield 2
        num >>= 1
    # start scan with 3 and step = 2
    scan_start: int = 3
    while num > 1:
        try:
            # try to get first prospect prime
            scan_start = next(divisors(num, start=scan_start, step=2))
        except StopIteration:
            # if no divisors, means num is prime
            scan_start = num
        yield scan_start
        num //= scan_start


def is_prime(num: int) -> bool:
    """
    Verify if num is prime
    :param num:
    :return: True if prime, False otherwise
    """
    assert num >= 1

    if num == 1:
        return False

    if num == 2:
        return True

    if num % 2 == 0:
        return False

    for _ in divisors(num, start=3, step=2):
        # try to get first divisor
        return False

    # if no divisors, than prime
    return True


def eval(num):
    return reduce(lambda x, y: x*10 + y, num)


def gen_numbers(n):
    digits_of_n = len(str(n))
    yield 2
    for num_of_digits in range(1, digits_of_n + 1):
        for num in itertools.product([1, 3, 5, 7, 9], repeat=num_of_digits):
            value = eval(num)
            if value < n:
                yield value
            else:
                return


def is_circular(i):
    i_str = str(i)
    ok = False
    for i in range(len(i_str)):
        num = i_str[i:] + i_str[:i]
        if not is_prime(int(num)):
            return False
    return True


def gen_circular_primes(n):
    for i in gen_numbers(n):
        if is_circular(i):
            yield i


circular = list(gen_circular_primes(10**6))
print(len(circular))
n = int(input())
print(sum(gen_circular_primes(n)))
