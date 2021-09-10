"""

The number, 197, is called a circular prime because all rotations of the digits:
    197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
Find the sum of circular primes that are below N?

"""

circular = [2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97]


def digits(n: int) -> Iterator[int]:
    """Iterate over digits of n from least significant to most significant digit."""
    yield n % 10
    n //= 10
    while n:
        yield n % 10
        n //= 10


def number_gen(n):
    pass

n = int(input())
