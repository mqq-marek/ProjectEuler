#!/bin/python3
"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below given number n.
"""

from bisect import bisect_right

SIEVE_SIZE = 2 * 10 ** 6 + 2
sieve = [0] * SIEVE_SIZE
primes = []


def binary_search(n):
    """Find element which contains pair (prime, sum_primes) with prime <= n."""
    i = bisect_right(primes, (n + 1, 0))
    return primes[i - 1][1]


def eratosthenes_sieve(arr):
    """ Build eratosthenes sieve and tuples of prime and primes cumulative sum. """
    primes.append((0, 0))
    prime = (2, 2)
    primes.append(prime)
    for i in range(3, SIEVE_SIZE, 2):
        if arr[i] == 0:
            primes.append((i, prime[1] + i))
            prime = primes[-1]
            for j in range(i + i, SIEVE_SIZE, i):
                arr[j] = 1


def hacker_main():
    eratosthenes_sieve(sieve)
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(binary_search(n))


def dev_main():
    eratosthenes_sieve(sieve)
    print(binary_search(2000000))


if __name__ == "__main__":
    hacker_main()
