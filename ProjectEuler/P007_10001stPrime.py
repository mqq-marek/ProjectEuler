#!/bin/python3
"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?
"""
import math

MAX_PRIME_NUMBER = 10001
APPROX_ERROR = 0.15
SIEVE_SIZE = int(math.log(MAX_PRIME_NUMBER) * (1+APPROX_ERROR) * MAX_PRIME_NUMBER) + 1
sieve = [0] * SIEVE_SIZE
primes = [0, 2]


def eratosthenes_sieve(arr):
    for i in range(3, SIEVE_SIZE, 2):
        if arr[i] == 0:
            primes.append(i)
            for j in range(i + i, SIEVE_SIZE, i):
                arr[j] = 1


if __name__ == "__main__":
    eratosthenes_sieve(sieve)
    # print(primes[10001])
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(primes[n])


