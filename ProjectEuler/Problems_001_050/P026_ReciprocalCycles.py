"""

A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions
with denominators 2 to 10 are given: 1/2 = 0.5, ...

Where 0.1(6) means 0.1666... and has 1-digit recurring cycle. 1/7 has 6 digit recurring cycle.

Find the value of smallest d<N for which 1/d contains the longest recurring cycle in its decimal fraction part.

"""
import math
import operator
from bisect import bisect_left
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
    assert num >= 1

    if num == 1:
        yield num
    # start scan with the lowest prime
    scan_start: int = 2
    while num > 1:
        try:
            # try to get first prospect prime
            scan_start = next(divisors(num, start=scan_start))
        except StopIteration:
            # if no divisors, means num is prime
            scan_start = num
        yield scan_start
        num //= scan_start

# element [0] - longest cycle until now
# element [1:] - number where max cycle length increases
first_cycle_number = [1, 3]


def ten_power(n):
    """ Find smallest 10**power > n. """
    nn = n
    power = 10
    while power < n:
        power *= 10
    return power


def find_cycle_len(divisor):
    """ Find cycle length for dividends prime against numbers without 2 and 5 divisors. """
    dividend = ten_power(divisor)
    results = set()
    while dividend not in results:
        results.add(dividend)
        quotient, reminder = divmod(dividend, divisor)
        dividend = 10 * reminder
    return len(results)


def recurring_cycle(n):
    """ Compute recurring cycle. """
    primes_except_2_5 = [d for d in prime_divisors(n) if d != 2 and d != 5]
    if primes_except_2_5:
        divisor = reduce(operator.mul, primes_except_2_5, 1)
        cycle_len = find_cycle_len(divisor)
        return cycle_len
    return 0


def init():
    """ Initialize table giving first number with the longest cycle below n. """
    for i in range(5, 10001, 2):
        cl = recurring_cycle(i)
        if cl > first_cycle_number[0]:
            first_cycle_number[0] = cl
            first_cycle_number.append(i)
    first_cycle_number.append(10001)
    first_cycle_number[0] = 1


def longest_recurring_cycle(n):
    """ Find smallest number with longest recurring cycle from table. """
    ndx = bisect_left(first_cycle_number, n)
    return first_cycle_number[ndx-1]


init()
# print(longest_recurring_cycle(1000))
t = int(input())
for _ in range(t):
    n = int(input())
    print(longest_recurring_cycle(n))
