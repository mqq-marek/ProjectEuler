"""

"""
import itertools


def sqrt2_seq():
    """Coefficient for sqrt(2) infinite fraction."""
    yield 1
    while True:
        yield 2


def e_seq():
    """Coefficient for e infinite fraction."""
    start = 2
    yield start
    yield 1
    while True:
        yield start
        yield 1
        yield 1
        start += 2


def fractions(seq):
    """
    Fractions numerator and denominator values  can be computed as W(i+2) = W(i) + coef * W(i+1).
    [Easy to find - just try to compute few initial values....]
    Numerator and denominator for W(0) and W(1) computed by definition.
    """
    den_0 = 1
    num_0 = next(seq)
    den_1 = next(seq)
    num_1 = num_0 * den_1 + 1
    yield num_0, den_0
    yield num_1, den_1
    for coefficient in seq:
        num_0, num_1 = num_1, num_0 + coefficient * num_1
        den_0, den_1 = den_1, den_0 + coefficient * den_1
        yield num_1, den_1


def digits_sum(num):
    """Digits sum for number."""
    return sum(int(d) for d in str(num))


def n_th_num_sum(n):
    """n-th element numerator sum of digits."""
    for num, den in itertools.islice(fractions(e_seq()), n):
        pass
    return digits_sum(num)

n = 100
n = int(input())
print(n_th_num_sum(n))