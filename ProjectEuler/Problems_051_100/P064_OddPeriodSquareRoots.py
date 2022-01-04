"""

All square roots are periodic when written as continued fractions and can be written in the form:
....

"""
import itertools
import math


def next_fraction(a, b, c, n):
    """ Get next fraction element for given a,b, c as: a + b / (sqrt(23) - c)."""
    # Steps: b / (sqrt(n) - c) -> b(sqrt(n) + c) / (n -c*c) -> sqrt(n) + c / (n - c*c) // b
    assert (n - c * c) % b == 0
    b = (n - c * c) // b
    a = c // b + 1
    c = a * b - c
    # fraction sqrt(n) - c must be less than 1
    too_big = (int(math.sqrt(n)) - c) // b
    a += too_big
    c += too_big * b
    return a, b, c


def period(n):
    """Compute period."""
    a = int(math.sqrt(n))
    if a * a == n:
        return 0
    b = 1
    c = a
    # The second element
    a, b, c = next_fraction(a, b, c, n)
    a1, b1, c1 = a, b, c
    for i in itertools.count():
        a, b, c = next_fraction(a, b, c, n)
        # Check against second element
        if a == a1 and b == b1 and c == c1:
            return i + 1


def verify_range(n):
    """Count odd periods."""
    return sum(period(num) % 2 == 1 for num in range(2, n + 1))


n = int(input())
# n = 10000
print(verify_range(n))








