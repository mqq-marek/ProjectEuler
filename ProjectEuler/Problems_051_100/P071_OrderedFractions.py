"""
Consider the fraction, n/d, where n and d are positive integers.
If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7,
    1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d <= 1,000,000 in ascending order of size, find
the numerator of the fraction immediately to the left of 3/7.

"""
import math
from fractions import Fraction


def eegcd(a, b):
    """Compute Extend Euclid GCD Algorithm.
    Return g, x, y such that:
    g = gcd/hcf(a, b)
    a * b // g = LCM(a, b)
    g = a * x + b * y
    """
    if a == 0:
        return b, 0, 1
    g, y, x = eegcd(b % a, a)
    return g, x - (b // a) * y, y


def find_naive(a, b, n):
    """Find c/d < a/b closest to a/b with fractions with denominator up to n."""
    divisor = math.gcd(a, b)
    a, b = a // divisor, b // divisor
    limit = a * n // b + 2
    c, d = 0, 1
    c_old, d_old = c, d
    cnt = 0
    for x in range(1, limit):
        y, rem = divmod(x * b, a)
        y += 1
        if y > n:
            break
        if d * x > c * y:
            eq = d * x == c * y
            mult = n // y
            divisor = math.gcd(x, y)
            c, d = x // divisor, y // divisor
            print(f'Better: {cnt:5}[{eq:1}]: {x * mult}/{y * mult} ({x}/{y}) '
                  f'[{x-c_old}:{y-d_old}], rem={rem}')
            cnt += 1
            d_old = y
            c_old = x
    mul = n // d
    print(f'Found {c}/{d} < {a}/{b} of {n} [{c*mul}/{d*mul}] {n} // {d}')
    print(f'{c}, {d}')
    return c, d


def find_fast(a, b, n):
    """Find c/d < a/b closest to a/b with fractions with denominator up to n."""
    a_b_gcd = math.gcd(a, b)
    a, b = a // a_b_gcd, b // a_b_gcd
    c, d = 0, 1
    best_rem = -1
    cnt = 0
    c_old, d_old = 0, 1
    for x in range(1, b + 2):
        y, rem = divmod(x * b, a)
        y += 1
        if y > n:
            # print(f'Early return: {c}/{d} [x, y: {x}/{y}')
            return c, d
        # print(f'Loop: divmod(x * b, a: {x} * {b}, {a}) = {y}, {rem}')
        condition1 = rem > best_rem
        condition2 = d * x > c * y
        assert condition1 == condition2, f"{a}/{b} > {x}/{y} rem: {rem}, {condition1}/{condition2}"
        if rem > best_rem:
            cnt += 1
            best_rem = rem
            a_b_gcd = math.gcd(x, y)
            # c, d = x // a_b_gcd, y // a_b_gcd
            c, d = x, y
            mult = n // y
            # print(f'Better: {cnt:5}: {x * mult}/{y * mult} ({x}/{y}) '
            #       f'diff: {diff(a, b, c, d)}[{x-c_old}:{y-d_old}], rem={rem}')
            d_old = y
            c_old = x
            if best_rem == a - 1:
                break
    print(f"Initial best {c}/{d}")
    multiply = (n - d) // b
    new_c = c + multiply * a
    new_d = d + multiply * b
    a_b_gcd = math.gcd(new_c, new_d)
    c, d = new_c // a_b_gcd, new_d // a_b_gcd
    # print(f'Found {c}/{d} < {a}/{b} of {n}  {n} // {d}')
    return c, d


def find_eegcd(a, b, n):
    """Find c/d < a/b closest to a/b with fractions with denominator up to n."""
    """Assumes gcd(a, b) == 1, n > b"""
    """Find c, d such that: (c * b) % a = (a -1) and d = c * b // a. """
    _, d, _ = eegcd(a, b)
    if d < 0:
        d += b
    c = a * d // b

    multiply = (n - d) // b
    new_c = c + multiply * a
    new_d = d + multiply * b
    a_b_gcd = math.gcd(new_c, new_d)
    c, d = new_c // a_b_gcd, new_d // a_b_gcd
    # print(f'Found {c}/{d} < {a}/{b} of {n}  {n} // {d}')
    return c, d


def test(a, b, n):
    # return find_fast(a, b, n)
    return find_naive(a, b, n)


test_n = 1000000
#
# assert test(119, 10**15-1, 8403361344537) == (0, 1)
# assert test(119, 10**15-1, 8403361344538) == (1, 8403361344538)
# assert test(119, 10**15-1, 50420168067227) == (6, 50420168067227)
# assert test(119, 10**15-1, 92436974789916) == (11, 92436974789916)
# assert test(119, 10**15-1, 134453781512605) == (16, 134453781512605)
# assert test(119, 10**15-1, 176470588235294) == (21, 176470588235294)
# assert test(119, 10**15-1, 218487394957983) == (26, 218487394957983)
# assert test(119, 10**15-1, 478991596638655) == (57, 478991596638655)
# assert test(119, 10**15-1, 739495798319327) == (88, 739495798319327)
# assert test(119, 10**15-1, 739495798319327 + test_n * 10**15-1) == (88 + test_n * 119,
#                                                                     739495798319327 + test_n * (10**15-1))
#
#
# assert test(119, 17419, 146) == (0, 1)
# assert test(119, 17419, 147) == (1, 147)
# assert test(119, 17419, 292) == (1, 147)
# assert test(119, 17419, 293) == (2, 293)
# assert test(119, 17419, 731) == (2, 293)
# assert test(119, 17419, 732) == (5, 732)
# assert test(119, 17419, 1902) == (5, 732)
# assert test(119, 17419, 1903) == (13, 1903)
# assert test(119, 17419, 3073) == (13, 1903)
# assert test(119, 17419, 3074) == (21, 3074)
# assert test(119, 17419, 4244) == (21, 3074)
# assert test(119, 17419, 4245) == (29, 4245)
# assert test(119, 17419, 5415) == (29, 4245)
# assert test(119, 17419, 5416) == (37, 5416)
# assert test(119, 17419, 5416 + test_n * 17419) == (37 + test_n * 119, 5416 + test_n * 17419)
# assert test(119, 17419, 22834) == (37, 5416)
# assert test(119, 17419, 22835) == (156, 22835)
#
#
#
# assert test(3, 7, 7) == (2, 5)
# assert test(3, 7, 11) == (2, 5)
# assert test(3, 7, 12) == (5, 12)
# assert test(3, 7, 18) == (5, 12)
# assert test(3, 7, 19) == (8, 19)
# assert test(3, 7, 25) == (8, 19)
# assert test(3, 7, 26) == (11, 26)
# assert test(3, 7, 33) == (14, 33)
# assert test(3, 7, 26 + test_n * 7) == (11 + test_n * 3, 26 + test_n * 7)
#
# assert test(3, 5, 5) == (1, 2)
# assert test(3, 5, 6) == (1, 2)
# assert test(3, 5, 7) == (4, 7)
# assert test(3, 5, 11) == (4, 7)
# assert test(3, 5, 12) == (7, 12)
# assert test(3, 5, 12 + test_n * 5) == (7 + test_n * 3, 12 + test_n * 5)
#
# assert test(4, 5, 5) == (3, 4)
# assert test(4, 5, 8) == (3, 4)
# assert test(4, 5, 9) == (7, 9)
# assert test(4, 5, 13) == (7, 9)
# assert test(4, 5, 14) == (11, 14)
# assert test(4, 5, 14 + test_n * 5) == (11 + test_n * 4, 14 + test_n * 5)
#
# assert test(6, 7, 7) == (5, 6)
# assert test(6, 7, 8) == (5, 6)
# assert test(6, 7, 9) == (5, 6)
# assert test(6, 7, 10) == (5, 6)
# assert test(6, 7, 11) == (5, 6)
# assert test(6, 7, 12) == (5, 6)
# assert test(6, 7, 13) == (11, 13)
# assert test(6, 7, 19) == (11, 13)
# assert test(6, 7, 20) == (17, 20)
# assert test(6, 7, 20 + test_n * 7) == (17 + test_n * 6, 20 + test_n * 7)
#
# assert test(1, 5, 6) == (1, 6)
# assert test(1, 5, 10) == (1, 6)
# assert test(1, 5, 11) == (2, 11)
# assert test(1, 5, 15) == (2, 11)
# assert test(1, 5, 16) == (3, 16)
# assert test(1, 5, 16 + test_n * 5) == (3 + test_n, 16 + test_n * 5)

# exit()


t = int(input())
for _ in range(t):
    a, b, n = map(int, input().split())
    find_fast(a, b, n)
    print(c, d)

