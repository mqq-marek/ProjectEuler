"""
The first two consecutive numbers to have two distinct prime factors are:
The first three consecutive numbers to have three distinct prime factors are:

Given N find all the K consecutive integers, where first integer is <=N to have exactly K distinct prime factors.
Print the first of these numbers in ascending order.

"""
import math


NUMBERS = [0] * (2 * 10**6 + 1)


def eratosthenes_sieve(n):
    """Generate number with divisor counter. 0 for primes."""

    def add_divisor(k):
        pos = k + k
        while pos < n:
            NUMBERS[pos] += 1
            pos += k

    for i in range(2, n):
        if not NUMBERS[i]:
            add_divisor(i)


def find (n, k):
    """Find consecutive numbers."""
    counter = 0
    kxk = k * k
    for i in range(6, n+1):
        for j in range(k):
            if NUMBERS[i + j] != k:
                break
        if j == (k - 1) and NUMBERS[i + j] == k:
            print(i)
    return counter


eratosthenes_sieve(2 * 10**6 + 1)

# find(1000000, 4)
n, k = map(int, input().split())
find(n, k)

