"""

The cube, 41063625 (345**3), can be permuted to produce two other cubes: 56623104 (384**3) and 66430125 (405**3).
In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.

"""
from collections import defaultdict

cube_map = defaultdict(list)


def get_key(i):
    """Get cube sorted digits."""
    return ''.join(sorted(str(i*i*i)))


def show_permutations(n, k):
    """Find and print k element permutations."""
    res = []
    for i in range(100, n+1):
        key = get_key(i)
        cube_map[key].append(i)
    for _, v in cube_map.items():
        if len(v) == k:
            res.append(v[0])
    res = sorted(res)
    for i in res:
        print(i*i*i)


n, k = 10**4, 5
n, k = map(int, input().split())
show_permutations(n, k)
