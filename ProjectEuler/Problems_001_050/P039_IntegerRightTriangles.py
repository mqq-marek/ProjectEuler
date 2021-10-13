"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c},
there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p <= 1000, is the number of solutions maximised?

"""

# For Pythagorean triangle a, b, c can be decomposed as k*(x**2-y**2), 2*k*x*y and k*(x**2+y**2).
# For a + b + c = n we have that c < n // 2 this gives us that x ** 2 < n // 2 and y**2 < n // 4 (as x > y)
import math
from collections import defaultdict

triangle_count = [0] * (5 * 10 ** 6 + 1)
best = [(0, 0)]


def triangle(n):
    """
    Find all triangles up to n and store results in triangle_count
        and best results in best.
    """
    # Search limit for x & y
    y_limit = int(math.sqrt(n) + 1) // 2
    x_limit = int(math.sqrt(n / 2) + 1)
    for y in range(1, y_limit):
        y2 = y * y
        for x in range(y + 1, x_limit):
            # basic/primitive triangle only when x, y coprime
            if math.gcd(x, y) != 1:
                continue
            x2 = x * x
            a = x2 - y2
            b = 2 * x * y
            c = x2 + y2
            if x % 2 and y % 2:
                # if x and y odd, then basic traingle need to be divided by 2 as a, b, c are even.
                a, b, c = a // 2, b // 2, c // 2
            a_b_c = a + b + c

            for k in range(1, n // a_b_c + 1):
                triangle_count[k * a_b_c] += 1

    best_value = 0

    for key, value in enumerate(triangle_count):
        if value > best_value:
            best_value = value
            best.append((key, best_value))


def find(n):
    """Find best perimeter."""
    best_key = 0
    for key, value in best:
        if key <= n:
            best_key = key
        else:
            break
    return best_key


triangle(5 * 10 ** 6 + 1)
print(triangle(1000))
k = int(input())
for _ in range(k):
    n = int(input())
    print(find(n))
