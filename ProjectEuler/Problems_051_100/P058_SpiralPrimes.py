"""

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting
is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 = 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed.
If this process is continued, what is the side length of the square spiral for which the ratio of primes along
both diagonals first falls below 10%?

+++
Diagonal numbers distance is increased by 8 with every new layer. The first diagonal in 4 directions
are 23, 5, 7, 9 and increase 10, 12, 14, 16. Each next increase is 8 larger.

Each increase add 4 new numbers which need to be verified as primes.

"""
import random
from bisect import bisect_left
import math
from typing import List


def eratosthenes_sieve(n):
    """Return primes <= n."""

    def add_prime(k):
        """Add founded prime."""
        primes.append(k)
        pos = k + k
        while pos <= n:
            numbers[pos] = 1
            pos += k

    numbers = [0] * (n + 1)
    primes = [2]
    for i in range(3, n + 1, 2):
        if not numbers[i]:
            add_prime(i)
    return primes


def is_prime(num: int, *, primes: List[int] = None) -> bool:
    """
    Verify if num is prime
    :param num:
    :param primes:
    :return: True if prime, False otherwise
    """
    if num < 2:
        return False

    if num in [2, 3]:
        return True

    if num % 2 == 0 or num % 3 == 0:
        return False

    max_n = int(math.sqrt(num))
    start = 5

    if primes and primes[-1] >= max_n:
        if num <= primes[-1]:
            return primes[bisect_left(primes, num)] == num
        for prime in primes:
            if prime > max_n:
                break
            if num % prime == 0:
                return False
        if primes[-1] % 6 == 1:
            start = primes[-1]
        else:
            start = primes[-1] + 2

        for n in range(start, 6, max_n + 1):
            if num % n == 0 or num % (n + 4) == 0:
                return False
        return True
    else:
        return is_prime_Miller_Rabin(num, primes=primes[:20])




def is_prime_Miller_Rabin(num: int, *, primes: List[int] = None, tests: int = 5) -> bool:
    """
    Verify if num is prime
    :param num:
    :param primes: initial sorted primes table if exist (e.g. from Eratosthenes) - recommend up to the first 20 primes
    :param tests: number of additional rounds for big number testing
    :return: True if prime, False otherwise
    """
    if num < 2:
        return False
    if num < 13:
        #       2,    3,    4,     5,    6,     7,    8,     9,     10,    11,   12
        return [True, True, False, True, False, True, False, False, False, True, False][num-2]

    sqrt_num = int(math.sqrt(num))
    for prime in primes:
        if prime > sqrt_num:
            return True
        if num % prime == 0:
            return False

    # Factor n-1 as d * 2 ** s
    s, d = 0, num - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Make witnesses
    if num < 1373653:
        test_set = [2, 3]
    elif num < 25326001:
        test_set = [2, 3, 5]
    elif num < 118670087467:
        if num == 3215031751:
            return False
        test_set = [2, 3, 5, 7]
    elif num < 2152302898747:
        test_set = [2, 3, 5, 7, 11]
    else:
        test_set = [2, 3, 5, 7, 11, 13] + [random.randrange(17, num - 1) for _ in range(tests)]
    for a in test_set:
        x = pow(a, d, num)
        if x in [1, num - 1]:
            continue
        for _ in range(s):
            x = x * x % num
            if x == num - 1:
                break
        else:
            return False
    return True


def is_in_sorted_list(primes, n):
    """Check if number is prime."""
    pos = bisect_left(primes, n)
    if pos < len(primes):  # n is in primes
        if primes[pos] == n:
            return True
    return False


def diagonal_numbers():
    """Return diagonals number for consecutive layers."""
    diagonals = [3, 5, 7, 9]
    increase = [10, 12, 14, 16]
    while True:
        yield diagonals
        diagonals = [a + b for a, b in zip(diagonals, increase)]
        increase = [i + 8 for i in increase]


def find_ratio(n):
    """Find layer with ratio less than n%."""
    primes = eratosthenes_sieve(150)
    numbers = 1
    prime_count = 0
    ratio = 100
    for diagonals in diagonal_numbers():
        prime_count += sum(is_prime_Miller_Rabin(num, primes=primes) for num in diagonals)
        numbers += 4
        new_ratio = prime_count * 100 // numbers
        # if new_ratio < ratio:
        #     ratio = new_ratio
        #     print(ratio, (numbers + 1) // 2, diagonals)
        if new_ratio < n:
            return (numbers + 1) // 2




#print(find_ratio(10))
n = int(input())
print(find_ratio(n))


