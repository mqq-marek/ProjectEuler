"""


Euler's Totient function, phi(n), is used to determine the number of positive
numbers less than or equal to n which are relatively prime to n.

For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, phi(9)=6.
The number 1 is considered to be relatively prime to every positive number, so phi(1)=1.

Interestingly, phi(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10**7, for which phi(n) is a permutation of n and the ratio n/phi(n) produces a minimum.

"""
import time
from bisect import bisect_right
from fractions import Fraction
import math
from collections import Counter
from typing import Iterator


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
    primes = [2]
    for i in range(n):
        if not numbers[i]:
            add_prime(i)
    return primes


primes = eratosthenes_sieve(10 ** 4)


def prime_divisors(num: int) -> Iterator[int]:
    """
    Get all num prime divisors.
    :param num: number for which we yields prime divisors
    :yields: num prime divisors
    """
    assert num > 0

    start_num = num
    sqrt_num = int(math.sqrt(num)) + 1
    counter = 0

    for p in primes:
        while num % p == 0:
            yield p
            counter += 1
            num //= p
        if num == 1 or counter > 3:
            return
        if p > sqrt_num:
            yield num
            return

    raise Exception(f"Primes too short for {start_num} -> {num}, Primes{len(primes)}/{primes[-1]}")


def totient(n):
    """ Compute totient.
    totient(prime**k) = p**k - p**(k-1)
    totient(n*m) = totient(n) * totient(m) if n,m coprime.
    """
    result = list(prime_divisors(n))
    prime_power = Counter(result)
    res = 1
    for p, cnt in prime_power.items():
        if cnt == 1:
            res *= (p - 1)
        else:
            res = pow(p, cnt - 1) * (p - 1)
    return res, result


def totient_loop_naive(n):
    index = 0
    ratio = Fraction(2, 1)
    start = time.perf_counter()
    cnt = 0
    for i in range(17, n):
        tt = totient(i)
        t = tt[0]
        if sorted(str(i)) == sorted(str(t)):
            new_ratio = Fraction(i, t)
            if new_ratio < ratio:
                # print(cnt, i, i - index, t, tt[1], round(float(new_ratio),3), round(time.perf_counter() - start))
                cnt += 1
                start = time.perf_counter()
                ratio = new_ratio
                index = i
    return index


def totient_guesser(n):
    ratio = n
    index = 0
    n_sqrt = int(math.sqrt(n)) + 1
    start = primes.index(149)
    end = bisect_right(primes, n_sqrt) + 1
    for i1 in range(start, end):
        p1 = primes[i1]
        for i2 in range(i1, len(primes)):
            p2 = primes[i2]
            p12 = p1 * p2
            if p12 >= n:
                break
            phi = (p1-1) * (p2 - 1)
            new_ratio = p12 / phi
            if new_ratio < ratio and sorted(str(p12)) == sorted(str(phi)):
                # print(p1, p2, new_ratio, p12)
                ratio = new_ratio
                index = p12
            for i3 in range(i2, len(primes)):
                p3 = primes[i3]
                p123 = p12 * p3
                if p123 >= n:
                    break
                phi *= (p3 - 1)
                new_ratio = p123 / phi
                if new_ratio < ratio and sorted(str(p123)) == sorted(str(phi)):
                    # print(p1, p2, new_ratio, p12)
                    ratio = new_ratio
                    index = p123
    return index


def totient_solver(n):
    if n <= 76000:
        return totient_loop_naive(n)
    return totient_guesser(n)


#n = 10**7
n = int(input())
print(totient_solver(n))
