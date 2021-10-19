"""

Compute amount ot element when C(n, r) < K for n <= N, 0<=r<=n

"""


def c_n_r_sequence(n):
    """Iterate the first half of C(n, r) sequence."""
    r = 0
    start = 1
    for r in range(0, n // 2 + 1):
        yield start
        start = start*(n-r)//(r+1)


def count(n, k):
    """Count amounts of elements greater than K"""
    for index, c in enumerate(c_n_r_sequence(n)):
        if c > k:
            return n + 1 - 2 * index
    return 0


def sum_c_n_r(n, k):
    """Count total for n in range N..1."""
    total = 0
    for i in range(n, 0, -1):
        cnt = count(i, k)
        total += cnt
        if cnt == 0:
            break
    return total


n, k = [int(s) for s in input().split()]
print(sum_c_n_r(n, k))


