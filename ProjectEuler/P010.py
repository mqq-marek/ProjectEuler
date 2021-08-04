#!/bin/python3

from bisect import bisect_right

SIEVE_SIZE = 10 ** 6 + 2
sieve = [0] * SIEVE_SIZE
primes = []


def binary_search(n):
    """Find element which contains pair (prime, sum_primes) with prime <= n."""
    i = bisect_right(primes, (n + 1, 0))
    return primes[i - 1][1]


def eratosthenes_sieve(arr):
    """ Build eratosthenes sive and tuples of prime and primes cumulative sum. """
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
    for i in range(20):
        print(i, binary_search(i))


if __name__ == "__main__":
    dev_main()
