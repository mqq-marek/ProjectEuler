""""
You have an infinite number of 4 types of lego blocks of sizes given as (depth x height x width):

d	h	w
1	1	1
1	1	2
1	1	3
1	1	4
Using these blocks, you want to make a wall of height  and width . Features of the wall are:

- The wall should not have any holes in it.
- The wall you build should be one solid structure,
    so there should not be a straight vertical break across all rows of bricks.
- The bricks must be laid horizontally.

How many ways can the wall be built?

Example
n = 2
m = 3

There are 9 valid permutations in all.

"""
import itertools
import operator
from functools import reduce

from core import partitions

MODULO = 10**9+7

rows_counter = {1: 1, 2: 2, 3: 4, 4: 8, 5: 15, 6: 29}
towers_counter = {}


def rows_permutation(m):
    if rows_counter.get(m) is None:
        rows_counter[m] = (2 * rows_permutation(m-1) - rows_permutation(m-5)) % MODULO
    return rows_counter[m]


def tower_permutation(n, m):
    if n == 1:
        if m <= 4:
            return 1
        return 0
    if m == 1:
        return 1
    if m == 2:
        return pow(2, n, MODULO) - 1
    if towers_counter.get((n, m)) is None:
        one_row_counter = rows_permutation(m)
        all_towers = pow(one_row_counter, n, MODULO)
        cut_partitions = partitions(m)
        next(cut_partitions)
        for p in cut_partitions:
            partition_product = 1
            for e in p:
                partition_product *= tower_permutation(n, e)
            partition_product *= len(set(itertools.permutations(p)))
            all_towers -= partition_product
        towers_counter[(n, m)] = all_towers % MODULO
    return towers_counter[(n, m)]


def row_patterns(m):
    """
    Find all possible way to build row size m from blocks [1, 2, 3, 4]
    :param m: row length
    :yield: combinations how row m can be build from different amounts of bricks 1, 2, 3, 4
    For m = 5 yields (5, 0, 0, 0), (3, 1, 0, 0), (2, 0, 1, 0), (1, 2, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0)
    """
    for i1 in range(0, m + 1):
        for i2 in range((m - i1) // 2 + 1):
            for i3 in range((m - i1 - i2 * 2) // 3 + 1):
                for i4 in range((m - i1 - i2 * 2 - i3 * 3) // 4 + 1):
                    if i1 + i2 * 2 + i3 * 3 + i4 * 4 == m:
                        yield i1, i2, i3, i4


def row_blocks(patterns):
    """
    Find all possible way how you can build row m with bricks 1, 2, 3, 4
    :param patterns:
    :yield: permutation of every row build with blocks 1, 2, 3, 4
    For m = 5 yields [1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 2, 1], [1, 2, 1, 1], [2, 1, 1, 1],
        [1, 1, 3], [1, 3, 1], [3, 1, 1], [1, 2, 2], [2, 1, 2], [2, 2, 1],
        [1, 4], [4, 1], [2, 3], [3, 2] in total 15 permutations
    """
    for l1, l2, l3, l4 in patterns:
        base_row = [1] * l1 + [2] * l2 + [3] * l3 + [4] * l4
        perm_rows = set(itertools.permutations(base_row))
        for r in perm_rows:
            yield r
            
            
def row_cuts(rows, m):
    """
    Build lego row representation by showing places where row is split between blocks.
    Row length m has max m-1 places where one brick ends and another one starts.
    For row length 5 composed of [2, 1, 2] yields [0, 1, 1, 0].
    :param rows: list of row blocks in order
    :param m: row length
    :yield: cuts for all rows which can be used 
    """
    for r in rows:
        cut = [0] * (m - 1)
        index = -1
        for block in r[:-1]:
            cut[index + block] = 1
            index += block
        yield cut
        
        
def count_towers(n, m):
    def check_tower():
        if n == 1:
            return 1
        for column in range(m - 1):
            sum = 0
            for row in range(n):
                sum += tower[row][column]
            if sum == n:
                return 0
        return 1

    blocks = list(row_blocks(row_patterns(m)))
    cuts = list(row_cuts(blocks, m))
    towers = itertools.product(cuts, repeat=n)
    tower_count = 0
    for tower in towers:
        tower_count += check_tower()
    elems = len(blocks)
    diff = elems ** n - tower_count
    print(f'For height={n} and length={m} we have {tower_count} solutions vs {elems ** n} diff: {diff}')
    # print(f'Solutions as primes {list(prime_divisors(tower_count))}')
    if diff:
        pass
        # print(f'Diff as primes {list(prime_divisors(diff))}')
    assert tower_count == tower_permutation(n, m)
    return tower_count


def legoBlocks(n, m):
    return tower_permutation(n, m)


def check_towers():
    assert legoBlocks(2, 2) == 3
    assert legoBlocks(3, 2) == 7
    assert legoBlocks(2, 3) == 9
    assert legoBlocks(4, 4) == 3375
    assert legoBlocks(4, 5) == 35714
    assert legoBlocks(4, 6) == 447902
    assert legoBlocks(4, 7) == 5562914
    assert legoBlocks(5, 4) == 29791
    assert legoBlocks(6, 4) == 250047
    assert legoBlocks(7, 4) == 2048383


def check_file():
    data = []
    result = []
    with open('lego_input.txt') as f:
        l = int(f.readline())
        for _ in range(l):
            n, m = map(int, f.readline().split())
            data.append((n, m))
    with open('lego_output.txt') as f:
        for _ in range(l):
            res = int(f.readline())
            result.append(res)

    for (n, m), r in zip(data, result):
        res = legoBlocks(n, m)
        if res != r:
            print(f'Fail with legoBlocks({n},{m}).\n - received: {res}, expected {r}')


if __name__ == "__main__":
    # check_towers()
    # check_file()
    for m in range(1, 21):
        m1 = rows_permutation(m)
        m2 = legoBlocks(2, m)
        m3 = legoBlocks(3, m)
        print(f'{m}\t{m1}\t{m2}\t{m3}')