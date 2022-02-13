"""
Euler's Totient function, phi(n), is used to determine the number of numbers
less than n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and
relatively prime to nine, phi(9)=6.
n 	Relatively Prime 	phi(n) 	n/phi(n)
2 	1 	1 	2
3 	1,2 	2 	1.5
4 	1,3 	2 	2
5 	1,2,3,4 	4 	1.25
6 	1,5 	2 	3
7 	1,2,3,4,5,6 	6 	1.1666...
8 	1,3,5,7 	4 	2
9 	1,2,4,5,7,8 	6 	1.5
10 	1,3,7,9 	4 	2.5

It can be seen that n=6 produces a maximum n/phi(n) for n <= 10.

Find the value of n <= 1,000,000 for which n/phi(n) is a maximum.

"""
from fractions import Fraction
import math
from collections import Counter
from typing import Iterator, Iterable, Tuple, List


def eratosthenes_sieve(n):
    """Return primes <= n."""

    def add_prime(k):
        """Add founded prime."""
        p = k + k + 3
        primes.append(p)
        pos = k + p
        while pos <= n:
            numbers[pos] = 1
            pos += p

    numbers = [0] * (n + 1)
    for i in range(n):
        if not numbers[i]:
            add_prime(i)
    return primes


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
        # - from 2 (1 already processed) or from start if greater than 2
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
        divisors_stack: List[int] = []
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


IntPair = Tuple[int, int]


def prime_factors_with_powers(num: int) -> List[IntPair]:
    """Return prime divisors of num as tuples (prime, counter)."""
    primes = Counter(prime_divisors(num))
    result = []
    for prime, power in sorted(primes.items()):
        result.append((prime, power))
    if not result:
        # num is prime
        result = [(num, 1)]
    return result


def totient(n: int) -> int:
    """ Compute totient.
    totient(prime**k) = p**k - p**(k-1)
    totient(n*m) = totient(n) * totient(m) if n,m coprime.
    """
    result = prime_factors_with_powers(n)
    res = 1
    # if n > 500000 and (n % 2 or n % 3 or n % 5 or n % 7 or n % 11 or n % 13 or n % 17):
    #     return n, 1
    for prime, power in result:
        if power == 1:
            res *= prime - 1
        else:
            res *= pow(prime, power - 1) * (prime - 1)
    return res


def best_totient(n):
    ratio = Fraction()
    index = 0
    for i in range(2, n + 1):
        t = totient(i)
        if t == i - 1:
            # Got prime, ratio low
            continue
        new_ratio = Fraction(i, t)
        if new_ratio > ratio:
            ratio = new_ratio
            index = i
            # print(i, ratio)
    return ratio, index


def best_totient_fast(n, primes):
    """Best index i multiply of prime numbers as it has the biggest number of divisors."""
    best_num = 1
    for p in primes:
        next = p * best_num
        if next >= n:
            return best_num
        best_num = next
    return


primes = eratosthenes_sieve(200)
t = int(input())
for _ in range(t):
    n = int(input())
    print(best_totient_fast(n, primes))
