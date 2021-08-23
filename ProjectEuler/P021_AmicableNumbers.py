"""

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and
each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284.
The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.

"""

import math
from collections import defaultdict
from typing import Iterator, Iterable

checked = [1, 1] + [0] * (10**5)
amicable = []


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


def sum_divisors(n):
    """ Sum all divisors except n. """
    div_sum = sum(divisors(n, start=1)) - n
    return div_sum


def add_amicable(n):
    """ Add amicable pair if n in it. Mark all related numbers as checked. """
    if checked[n]:
        return
    ns = sum_divisors(n)
    checked[n] = ns
    while True:
        if ns < len(checked) and checked[ns]:
            return
        ms = sum_divisors(ns)
        if ns < len(checked):
            checked[ns] = ms
        if ms == n:
            amicable.append(n)
            amicable.append(ns)
            return
        if ns >= len(checked):
            return
        n, ns = ns, ms


def sum_amicable(n):
    """ Find all amicable numbers using count down and compute sum. """

    # Remember current n for next search as way to limit search space.
    # Initially search from n to 1.
    start = checked[0]
    checked[0] = max(n, start)

    for i in range(n, start, -1):
        add_amicable(i)

    result = sum(i for i in amicable if i < n)

    return result


# print(sum_amicable(10000))
t = int(input())
for _ in range(t):
    n = int(input())
    print(sum_amicable(n))
