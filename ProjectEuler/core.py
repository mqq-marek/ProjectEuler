"""
Gems or core functionalities used in different problems.
"""
import operator
from functools import reduce
import math
from typing import Iterator, Sequence, TypeVar, Callable

GenT = TypeVar('T')


def sequence_condition(condition: Callable[[GenT, GenT], bool], sequence: Sequence[GenT]) -> bool:
    """
    Verify if sequence fulfill operator condition between current and next element.
    :param condition: operator define condition between item[i] and item[i+1]
    :param sequence:
    :return: True if condition is True for all pairs (i, i+1)
    """
    return all(condition(item1, item2) for item1, item2 in zip(sequence, sequence[1:]))


def fibonacci() -> Iterator[int]:
    """
    Fibonacci numbers generator.
    :yields: fibonacci sequence: 0, 1, 1, 2, 3, 5
    """
    f_current: int = 0
    f_next: int = 1
    while True:
        yield f_current
        f_current, f_next = f_next, f_current + f_next


def divisors(num: int, /, start: int = 2, ordered: bool = False) -> Iterator[int]:
    """
    Get all number divisors starting from start.
    Faster (sqrt(n) operations) than scanning all numbers using:
        divisors = (i for i in range(start, n) if n % mod i == 0).
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
    assert num > 0, "divisors iterator works with num > 0"
    assert start > 0, "divisors iterator works with start > 0"
    # 1, 2, 3 is special case yields [1], [1, 2] or [1, 3] for start = 1 empty list otherwise
    if num in [1, 2, 3]:
        if start == 1:
            yield 1
            if num > 1:
                yield num
        return
    # find divisors until sqrt(num)
    sqrt_num: int = int(math.sqrt(num))
    # return nothing if you start is above sqrt(num)
    if start > sqrt_num:
        return
    # Keep here half of divisors if ordered list of divisors is requested
    divisors_list: [int] = []
    # look for divisors from start until sqrt_num, but not including sqrt_num as it special case
    for j in range(start, sqrt_num):
        if num % j:
            continue
        # when j is divisor then also num // j is divisor
        yield j
        # divisors(21, 1) yields 1, 21, 3, 7
        if ordered:
            # keep second divisor in list as it is not in increasing order
            # yields 1, 3 from this loop and 7, 21 form list in traversed in reversed order
            divisors_list.append(num // j)
        else:
            # or yield them directly if order is not important
            yield num // j
    if num % sqrt_num == 0:
        # if sqrt_num divides num, we also emit it (no part of previous loop)
        yield sqrt_num
        if num // sqrt_num != sqrt_num:
            # and yield also num // sqrt_num in case when sqrt_num**2 is not equal num.
            # this prevents yields double sqrt_num when num is sqaure of integer
            yield num // sqrt_num
    for divisor in reversed(divisors_list):
        yield divisor


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


def least_common_multiple(seq: Sequence[int]) -> int:
    """
    Least common multiple of positive integers.
    :param seq: sequence of numbers
    :return: LCM
    """
    def lcm(num1: int, num2: int) -> int:
        return num1 * num2 // math.gcd(num1, num2)

    return reduce(lcm, seq, 1)
