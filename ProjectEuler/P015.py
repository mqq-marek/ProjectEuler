"""

Starting in the top left corner of a  2x2 grid, and only being able to move to the right and down,
there are exactly 6 routes to the bottom right corner.

result = (n+m)! / n! / m!

"""

import math
# print(math.factorial(40)//(math.factorial(20)**2))
mod = 10**9 + 7
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    i = min(n, m)
    j = max(n, m)
    res = 1
    for k in range(i):
        res *= j + k + 1
    res //= math.factorial(i)
    print(res % mod)