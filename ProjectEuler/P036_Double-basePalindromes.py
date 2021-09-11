"""
The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base K.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""
from typing import Iterator


def digits(n: int, base: int = 10) -> Iterator[int]:
    """Iterate over digits of n from least significant to most significant digit."""
    yield n % base
    n //= base
    while n:
        yield n % base
        n //= base


def is_double(n, k):
    n_10 = list(digits(n, base=10))
    if not n_10 == n_10[::-1]:
        return False
    n_k = list(digits(n, base=k))
    return n_k == n_k[::-1]


def gen_doubles(n, k):
    for i in range(n):
        if is_double(i, k):
            yield i


# print(sum(gen_doubles(10**6, 2)))
n, k = map(int, input().split())
print(sum(gen_doubles(n, k)))
