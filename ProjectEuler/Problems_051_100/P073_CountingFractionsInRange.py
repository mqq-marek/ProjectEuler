"""

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1,
it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d <= 12,000?

"""
import itertools
import math
from collections import namedtuple, Counter
from fractions import Fraction
from typing import List, NamedTuple, Iterator


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


def count_rationals_simple(a, d):
    """
    Count rationals between 1/(a+1) and 1/a where max enumerator is d.
    """
    fractions = 0
    frs = set()
    for y in range(a + 2, d + 1):
        x_min, rem = divmod(y, a + 1)
        x_min += 1
        x_max, rem = divmod(y, a)
        if rem == 0:
            x_max -= 1
        if x_max < x_min:
            continue
        for x in range(x_min, x_max + 1):
            g = math.gcd(x, y)
            if g == 1:
                fractions += 1
                frs.add(Fraction(x, y))
    frs = sorted(((f.numerator, f.denominator) for f in frs), key=lambda s: s[1])
    # print(frs)
    return fractions


"""Classes for representing fractions as: j / k * a + l for analysis."""


class Var(NamedTuple):
    """Represent number as x1 * a + x0."""
    x1: int
    x0: int

    def add(self, other: 'Var') -> 'Var':
        return Var(x1=self.x1 + other.x1, x0=self.x0 + other.x0)

    def value(self, x1: int):
        return self.x1 * x1 + self.x0

    def __str__(self):
        if self.x1:
            return f"{self.x1}*a+{self.x0}"
        else:
            return f"{self.x0}"


class VarFraction(NamedTuple):
    """Represent fraction as numerator and denominator."""
    num: Var
    den: Var

    def mid_fraction(self, other: 'VarFraction') -> 'VarFraction':
        """Build fraction which can be placed between left and right fractions."""
        result = VarFraction(num=self.num.add(other.num), den=self.den.add(other.den))
        assert result.num.x1 == 0
        print(f"{result} <= {self} + {other}")
        return result

    def value(self, a: int) -> Fraction:
        return Fraction(self.num.x1 * a + self.num.x0, self.den.x1 * a + self.den.x0)

    def __str__(self):
        return f"{self.num}/{self.den}"


class Range(NamedTuple):
    """Represent two closed fraction."""
    fr: VarFraction
    to: VarFraction


def count_rationals_semi_recursive(a, d):
    """
    Generate fractions between 1/(a+1) and 1/a where max enumerator is d
    """
    fr = VarFraction(num=Var(x1=0, x0=1), den=Var(x1=1, x0=1))
    to = VarFraction(num=Var(x1=0, x0=1), den=Var(x1=1, x0=0))
    fractions: List[VarFraction] = []
    generator: List[Range] = [Range(fr=fr, to=to)]

    for g in generator:
        new = g.fr.mid_fraction(g.to)
        # print(new, new.value(a), new.den.value(a), d)
        if new.den.value(a) <= d:
            fractions.append(new)
            generator.append((Range(fr=g.fr, to=new)))
            generator.append((Range(fr=new, to=g.to)))
    fr = sorted(fractions, key=lambda x: (x.den.x1, x.den.x0, x.num.x0))
    for key, gr in itertools.groupby(fr, key=lambda x: x.den.x1):
        grl = list(gr)
        gr_str = ', '.join([repr((r.num.x0, r.den.x1, r.den.x0)) for r in grl])
        print(f"{key:2}[{len(grl):3}]: {gr_str}")

    return fractions


def count_rationals_by_expression(a, d):
    """
    Count fractions between 1/(a+1) and 1/a where max enumerator is d.
    Generate fractions with the following denominators:
    2a+1
    3a+2, 3a+1
    4a+3, 4a+1
    5a+4, ..., 5a+1
    6a+5, 6a+1
    7a+6, 7a+5,...,7a+2,7a+1

    k*a + i and k, i coprime, so we have totient(k) elements here

    """
    k = 2
    total = 0
    while (k + 1) * a - 1 <= d:
        total += totient(k)[0]
        k += 1
    if k * a + 1 >= d:
        total += 1

    for i in range(2, d - k * a + 1):
        if k % i:
            total += 1
    # print(limit, last, d - last + i)

    # frs = set()
    # ax2 = a + a
    # ap1x2 = 2 * (a + 1)
    # even_left = (d + 1) // ap1x2
    # for i in range(even_left):
    #     frs.add(Fraction())
    # even_right = (d - 1) // ax2
    # odd = (d - a - 1) // ax2
    # previous_odd = odd * (odd - 1)
    # current_odd = min(2 * odd, d - a * (2 * odd + 1))
    # total = max(0, even_left + even_right + previous_odd + current_odd - 1)
    # print(even_right, even_left, previous_odd, current_odd, odd)
    return total


# frac = count_rationals_semi_recursive(2, 200)

# a, d = map(int, input().split())
a, d = 2, 1000
# print(count_rationals_semi_recursive(a, 10000))
# print(count_rationals_by_expression(a, 10000))
for i in range(2, 20):
    print("r:", i, count_rationals_simple(2, i), count_rationals_by_expression(2, i))
# assert count_rationals_semi_recursive(2, 8) == 3
# assert count_rationals_semi_recursive(2, 10) == 4
# assert count_rationals_semi_recursive(2, 100) == 505
# assert count_rationals_semi_recursive(2, 1000) == 50695
# assert count_rationals_semi_recursive(2, 10000) == 5066251
# print(count_rationals_simple(a, d))
# print(count_rationals_semi_recursive(a, 10))
#
