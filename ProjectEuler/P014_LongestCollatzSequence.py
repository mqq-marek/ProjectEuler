"""
The following iterative sequence is defined for the set of positive integers:

n -> n/2 (n is even)
n -> 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms.
Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.

"""
from bisect import bisect_left

# at position n keeps colatz(n) if computed or 0
colatz_cache = [0] * (5 * 10 ** 6 + 2)
colatz_cache[2] = 1
# Keeps in table best n/colatz(n) pairs such that for i<n colatz(i) <= colatz(n)
# Last element is sentry and keeps max element computed until now, not necessary optimal, so its len is -1.
best_n_len_tab = [(1, 0), (2, 1), (3, -1)]
"""
# table build up to 5*10**7
best_n_len_tab = [(1, 0), (2, 1), (3, 7), (6, 8), (7, 16), (9, 19), (18, 20), (19, 20), (25, 23), (27, 111), (54, 112),
             (55, 112), (73, 115), (97, 118), (129, 121), (171, 124), (231, 127), (235, 127), (313, 130), (327, 143),
             (649, 144), (654, 144), (655, 144), (667, 144), (703, 170), (871, 178), (1161, 181), (2223, 182),
             (2322, 182), (2323, 182), (2463, 208), (2919, 216), (3711, 237), (6171, 261), (10971, 267), (13255, 275),
             (17647, 278), (17673, 278), (23529, 281), (26623, 307), (34239, 310), (35497, 310), (35655, 323),
             (52527, 339), (77031, 350), (106239, 353), (142587, 374), (156159, 382), (216367, 385), (230631, 442),
             (410011, 448), (511935, 469), (626331, 508), (837799, 524), (1117065, 527), (1126015, 527),
             (1501353, 530), (1564063, 530), (1723519, 556), (2298025, 559), (3064033, 562), (3542887, 583),
             (3732423, 596), (5649499, 612), (6649279, 664), (8400511, 685), (11200681, 688), (14934241, 691),
             (15733191, 704), (31466382, 705), (31466383, 705), (36791535, 744)]
"""


def binary_search_pairs(table, n):
    """Find element which contains pair (pos, len) with pos <= n."""
    i = bisect_left(table, (n + 1, 0)) - 1
    if table[i][1] == -1:
        i -= 1
    return i


def collatz(n):
    """
    Return collatz sequence length.
    f(n) = 1 + f(n//2) if n is even
    f(n) = 1 + f(3*n+1) if n is odd
    Keep computed values in colatz_cache.
    Implement recursion by visited table
    which is used for keeping intermediate steps
    and update colatz_cache.
    """

    if n < 2:
        return 0
    # if already computed return value from cache
    if n < len(colatz_cache) and colatz_cache[n]:
        return colatz_cache[n]
    # count and scan not know yet intermediate values
    count = 0
    visited = []
    while True:
        visited.append(n)
        count += 1
        if n % 2:
            n = 3 * n + 1
        else:
            n = n // 2
        # if value for next n is in cache:
        if n < len(colatz_cache) and colatz_cache[n]:
            # revisit intermediate steps in reverse order and store respective colatz value in cache.
            for i, j in enumerate(visited[::-1], 1):
                if j < len(colatz_cache):
                    colatz_cache[j] = colatz_cache[n] + i
            return colatz_cache[n] + count


def longest_up_to(n):
    """ Find last longest colatz sequence for i <= n."""

    def update_best_tab(n, len):
        """Update best_n_len table."""
        if best_n_len_tab[-1][1] == -1:
            # if sentry replace it
            best_n_len_tab[-1] = (n, len)
        else:
            best_n_len_tab.append((n, len))

    index = binary_search_pairs(best_n_len_tab, n)
    best_n, best_len = best_n_len_tab[index]

    for pos, val in best_n_len_tab[index + 1:-1]:
        if val == best_len and pos <= n:
            best_n = pos
        if val > best_len:
            return best_n

    for i in range(best_n_len_tab[-1][0], n + 1):
        seq_len = collatz(i)
        if seq_len >= best_len:
            # Find next best result
            update_best_tab(i, seq_len)
            best_len = seq_len
            best_n = i

    # add sentry for restart scanning
    update_best_tab(n + 1, -1)
    return best_n


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        seq_pos = longest_up_to(n)
        print(seq_pos)


def dev_main():
    print(longest_up_to(10))
    print(best_n_len_tab)
    print(longest_up_to(15))
    print(best_n_len_tab)
    print(longest_up_to(20))
    print(best_n_len_tab)

    for i in range(53, 57):
        pass
        # print(longest_up_to(i))
    for i in range(17, 21):
        pass
        print(i, longest_up_to(i))


dev_main()
