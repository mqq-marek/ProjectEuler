"""

It is possible to show that the square root of two can be expressed as an infinite continued fraction:
1 + 1 / (2 + 1/(2 + 1 / (2 + .......... )))

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2
1 + 1 / (2 + 1/2) = 7/5
1 + 1 / (2 + 1/(2 + 1/2)) = 17/12
1 + 1 / (2 +1 / (2 + 1 / (2 + 1/2))) = 41/29


The next three expansions are 99/70, 239/169, 577/408, but the eighth expansion 1393/985, is the first example
where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than the denominator?

+++++
Fractional part is: 1/2, 2/5, 5/12, 12/29, 29/70, 70/169, ...
so ff(n+2) = 2*ff(n+1) + ff(n) frac(i) = ff((i+1)//2) // ff(i//2 + 1)

"""
from itertools import islice


def ff():
    """Generate fraction numerators/denominators."""
    a, b = 1, 2
    yield a
    yield b
    while True:
        a, b = b, 2 * b + a
        yield b


def frac():
    """Generate recursive fraction part."""
    ff_iter = ff()
    a, b = next(ff_iter), next(ff_iter)
    while True:
        yield a, b
        a, b = b, next(ff_iter)


def one_plus_frac():
    """Add 1 to recursive fraction."""
    for a, b in frac():
        yield a + b, b


def is_condition():
    """Verify if amount of digits in numerator is greater than in denominator."""
    for a, b in one_plus_frac():
        yield len(str(a)) > len(str(b))

def print_condition(n):
    """Print sequence number when amount of digits in numerator is greater than in denominator."""
    iter = is_condition()
    for i in range(n):
        if next(iter):
            print(i+1)


# print(sum(islice(is_condition(), 1000)))
n = int(input())
print_condition(n)

