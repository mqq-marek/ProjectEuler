"""
It was proposed by Christian Goldbach that every odd composite number
can be written as the sum of a prime and twice a square.

You are given N, print the number of ways N can be represented as a sum of prime and twice a square.

"""
import math


def gen_primes(n: int) -> list[int]:
    """Gen odd primes."""
    def has_prime_divisors(k: int) -> bool:
        k_sqrt = math.sqrt(k)
        for p in primes:
            if k % p == 0:
                return True
            if p > k_sqrt:
                return False

    primes = [3, 5, 7, 11, 13]
    for i in range(15, n + 1, 2):
        if not has_prime_divisors(i):
            primes.append(i)
    return primes


PRIMES = gen_primes(5 * 10 ** 5 + 1)


def is_double_sqrt(n: int) -> bool:
    n_sqrt = int(math.sqrt(n // 2))
    return (n_sqrt * n_sqrt) == n // 2


def composition(n: int) -> int:
    count = 0
    for p in PRIMES:
        if p >= n:
            break
        if is_double_sqrt(n - p):
            count += 1
    return count


def project_euler():
    for i in range(9, 10**5+1, 2):
        if i not in PRIMES:
            if composition(i) == 0:
                print(i)
                return


# project_euler()
t = int(input())
for _ in range(t):
    n = int(input())
    print(composition(n))

