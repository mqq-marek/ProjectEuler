"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits
from left to right, and remain prime at each stage: 3797, 797, 97, and 7.
Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

"""
from itertools import product
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


def truncatable_right_to_left(n):
    """Generate truncatable numbers starting from two digits numbers."""
    # The first digit must be prime
    current = [2, 3, 5, 7]
    for digits in range(2, len(str(n))+1):
        truncatable = []
        # Next digit must be odd.
        for prime, right_digit in product(current, [1, 3, 5, 7, 9]):
            candidate = prime * 10 + right_digit
            if candidate >= n:
                return
            if is_prime(candidate):
                yield candidate
                truncatable.append(candidate)
        current = truncatable


def left_to_right_numbers(n: int) -> Iterator[int]:
    """Generate left to right numbers.
    For 234 generates 4, 34."""
    num = str(n)
    for i in range(1, len(num)):
        yield int(num[-i:])


def is_truncatable_left_to_right(n: int) -> bool:
    """Check for being truncatable in revers order."""
    for num in left_to_right_numbers(n):
        if not is_prime(num):
            return False
    return True


def truncatable(n):
    """Generate fully truncatable numbers up to n."""
    for i in truncatable_right_to_left(n):
        if is_truncatable_left_to_right(i):
            yield i


#print(sum(truncatable(10**19+1)))
n = int(input())
print(sum(truncatable(n)))