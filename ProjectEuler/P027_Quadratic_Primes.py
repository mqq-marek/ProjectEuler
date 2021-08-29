"""
Euler discovered the remarkable quadratic formula:
    n*n + n + 41

It turns out that the formula will produce 40 primes for the consecutive integer values 0 <= n <= 39.
However, when n = 40, 40*40 + 40 + 41 is divisible by 41, and certainly when n=41, 41*41 + 41 + 41
is clearly divisible by 41.

The incredible formula  n*n - 79 * n + 1601 was discovered, which produces 80 primes for
the consecutive values 0<= n <= 79. The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form: n*n + a*m + b, where  |a| <= N and |b| <= N

Find the coefficients, a and b, for the quadratic expression that produces
the maximum number of primes for consecutive values of n, starting with n = 0.

"""

import math
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

    try:
        # try to get first divisor
        _ = next(divisors(num, start=3, step=2))
    except StopIteration:
        # if no divisors, means num is prime
        return True
    else:
        return False


primes = [2, 3, 5, 7, 11, 13]


def quadtratic_coefficients(n):
    """ Brute force cooeficiendt finder. """
    best_a = 0
    best_b = 3
    best_len = 1
    for b in primes:
        # b must be prime as solution starts from n = 0, so b must be prime
        if b > n:
            break
        for a in range(- (b - 1), n+1):
            # for n = 1 result must be 2 or more, so a can not be smaller than -(b -1)
            ndx = 1
            while True:
                candidate = ndx*ndx + a * ndx + b
                # next candidate must be positive and prime
                if candidate >= 2 and is_prime(candidate):
                    ndx += 1
                else:
                    break
            if ndx > best_len:
                best_a = a
                best_b = b
                best_len = ndx - 1
    return best_a, best_b


def init():
    """Initialize primes table with values up to 2000. """
    for i in range(15, 2001, 2):
        if is_prime(i):
            primes.append(i)


init()
# print(quadtratic_coefficients(1000))
N = int(input())
a, b = quadtratic_coefficients(N)
print(a, b)

