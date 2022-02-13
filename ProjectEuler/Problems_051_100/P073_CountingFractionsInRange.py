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




def count_rationals_simple(a, d):
    """
    Count rationals between 1/(a+1) and 1/a where max enumerator is d.
    """
    fractions = 0
    frs = set()
    for y in range(2 * a + 1, d + 1):
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


def count_rationals(a, max_d):
    """
    Count rationals between 1/(a+1) and 1/a where max enumerator is d.
    Rational sequence properties:
    For given d if a/b and c/d as two consecutive rationals, then:
    1) b * c = a * d + 1
    2) Next rational between them is (a + c) / (b + d)
    So when a/b and c/d are two consecutive rational then next will be(a&b co-prime, c&d co-prime):
    (k*c - a) / (k*d - b) where k is max number such that k * d - b <= max_d
    """
    if max_d <= 2 * a:
        return 0
    fractions = 0
    rationals = []
    fa = 1
    fb = a + 1
    k = (max_d + 1) // (a + 1)
    fc = k
    fd = k * (a + 1) - 1
    while fc != 1 and fd != a:
        rationals.append((fc, fd))
        fractions += 1
        k = (max_d + fb) // fd
        fe = k * fc - fa
        ff = k * fd - fb
        this_gcd = math.gcd(fe, ff)
        fe, ff = fe // this_gcd, ff // this_gcd
        fa, fb, fc, fd = fc, fd, fe, ff
    # print(rationals)
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



a, d = map(int, input().split())

# for a in range(2, 10):
#     for d in range(2 * a + 1, 5 * a):
#         print(a, d, count_rationals_simple(a, d), count_rationals(a, d))

print(count_rationals(a, d))
