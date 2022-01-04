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
    a1 = next(seq)
    a2 = 1
    b2 = next(seq)
    b1 = a1 * b2 + 1
    yield a1, a2
    yield b1, b2
    for n in seq:
        a1, b1 = b1, a1 + n * b1
        a2, b2 = b2, a2 + n * b2
        yield b1, b2


def digits_sum(n):
    """Digits sum for number."""
    return sum(int(d) for d in str(n))


def n_th_num_sum(n):
    """n-th element numerator sum of digits."""
    for num, den in itertools.islice(fractions(e_seq()), n):
        pass
    return digits_sum(num)

n = 100
n = int(input())
print(n_th_num_sum(n))