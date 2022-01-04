"""

Consider quadratic Diophantine equations of the form:

x**2 – D*y**2 = 1

For example, when D=13, the minimal solution in x is 649**2 – 13×180*2 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

3**2 – 2×2**2 = 1
2**2 – 3×1**2 = 1
9**2 – 5×4**2 = 1
5**2 – 6×2**2 = 1
8**2 – 7×3**2 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.

"""
import itertools
import math

"""

x**2 - D*y**2 = 1
(x**2 - 1) / y**2 = D
sqrt(D) ~ x/y
Can be proof that some approximation of infinite sqrt(D) fraction is solution.

"""


def next_fraction(a, b, c, n):
    """Build infinite fraction coefficients."""
    """Get next fraction element for given a,b, c as: a + b / (sqrt(23) - c)."""
    # Steps: b / (sqrt(n) - c) -> b(sqrt(n) + c) / (n -c*c) -> sqrt(n) + c / (n - c*c) // b
    b = (n - c * c) // b
    a = c // b + 1
    c = a * b - c
    # fraction sqrt(n) - c must be less than 1
    too_big = (int(math.sqrt(n)) - c) // b
    a += too_big
    c += too_big * b
    return a, b, c


def sqr_seq(n):
    """Yield infinite fraction coefficients."""
    a = int(math.sqrt(n))
    if a * a == n:
        yield 0
        return
    yield a
    b = 1
    c = a
    # The second element
    a, b, c = next_fraction(a, b, c, n)
    yield a
    a1, b1, c1 = a, b, c
    for i in itertools.count():
        a, b, c = next_fraction(a, b, c, n)
        yield a


def fractions(seq):
    """
    Fractions numerator and denominator values  can be computed as W(i+2) = W(i) + coef * W(i+1).
    [Easy to find - just try to compute few initial values....]
    Numerator and denominator for W(0) and W(1) computed by definition.
    """
    den_0 = 1
    num_0 = next(seq)
    if not num_0:
        yield 0, 0
        return
    den_1 = next(seq)
    num_1 = num_0 * den_1 + 1
    yield num_0, den_0
    yield num_1, den_1
    for coefficient in seq:
        num_0, num_1 = num_1, num_0 + coefficient * num_1
        den_0, den_1 = den_1, den_0 + coefficient * den_1
        yield num_1, den_1


def solve(d):
    """Find solution for given d."""
    cnt = 0
    for x, y in fractions(sqr_seq(d)):
        if x == 0 or x * x - d * y * y == 1:
            return x


def find_best_x(n):
    max_x = 0
    for i in range(2, n + 1):
        if int(math.sqrt(i)) ** 2 < i:
            x = solve(i)
            if x > max_x:
                max_x = x
                max_i = i
    return max_i, max_x


n = 1000
n = int(input())
print(find_best_x(n)[0])




