"""
In England the currency is made up of pound and pence. There are eight coins in general circulation:
    1p, 2p, 5p, 10p, 20p, 50p 1GPB(100p) and 2GBP(200p).

How many different ways can N pence be made using any number of coins?
As the result can be large print answer mod 10**9 + 7.

"""
from typing import Iterator

SIZE = 10**5 + 1
MOD = 10**9 + 7

coin_values = [1, 2, 5, 10, 20, 50, 100, 200]
COINS_AMOUNT = 8


def coin_partitions(n, coin_types=COINS_AMOUNT) -> Iterator[list[int]]:
    """
    Yields number n partitions using 1, 2, 5, 10, 20, 50, 100 and 200.
    Partition i represented as 8 element array showing amount of every cons:
    [0, 1, 2, 0, 0, 0, 0, 1] = 207.
    """

    def update_partition(value, k=COINS_AMOUNT):
        """Build partition having smallest number of coins."""
        # print('update', value, k)
        for ndx in reversed(range(k)):
            partition[ndx], value = divmod(value, coin_values[ndx])

    def next_partition() -> bool:
        """
        Update in-place partition to the next one.
        :return: True if next partition exist otherwise False
        """
        if partition[0] == n:
            return False
        for i in range(1, COINS_AMOUNT):
            if partition[i]:
                partition[i] -= 1
                update_partition(partition[0] + coin_values[i], i)
                return True

    # Build partitions in order based on shortest partition length starting.
    if coin_types > COINS_AMOUNT:
        coin_types = COINS_AMOUNT
    cnt = 0
    partition = [0] * COINS_AMOUNT
    update_partition(n, coin_types)
    # print(partition)
    yield partition[:]
    while next_partition():
        cnt += 1
        # print(partition)
        yield partition[:]


def show_ranges(max_value):
    """Show structure of numbers depend on amount of coins."""
    for n in range(1, max_value + 1):
        counters = []
        for k in range(1, 9):
            lst = list(coin_partitions(n, k))
            counter = len(lst)
            assert ways_recursive(n, k - 1) == counter
            counters.append(counter)
        counters_str = '\t'.join(str(n) for n in counters)
        print(str(n) + '\t' + counters_str)


def ways_recursive(value, coin_index):
    """Recursive version."""
    if value == 0 or coin_index == 0:
        return 1
    if coin_index == 1:
        return 1 + value // 2
    if value < coin_values[coin_index]:
        return ways_recursive(value, coin_index - 1)
    else:
        return (ways_recursive(value, coin_index - 1) +
                ways_recursive(value - coin_values[coin_index], coin_index))


cache = [[], []] + [[0] * (10**5 + 1)] * (COINS_AMOUNT - 2)


def ways(value, coin_index):
    """First version with cache."""
    if value == 0 or coin_index == 0:
        return 1
    if coin_index == 1:
        return 1 + value // 2
    if cache[coin_index][value]:
        return cache[coin_index][value]
    if value < coin_values[coin_index]:
        result = ways(value, coin_index - 1)
    else:
        result = 0
        offset = value % coin_values[coin_index]
        for i in range(offset, value+1, coin_values[coin_index]):
            result += ways(i, coin_index - 1)
    cache[coin_index][value] = result
    return result

prev = [1]*SIZE
cur = [1]*SIZE

def ways_init():
    """Initialize table for final version."""
    for i in range(SIZE):
        cur[i] = 1 + i // 2
    for c in range(2, 8):
        prev = cur[:]
        for o in range(coin_values[c]):
            cur[o] = prev[o]
        for o in range(coin_values[c]):
            a = prev[o]
            for i in range(o+coin_values[c], SIZE, coin_values[c]):
                b = prev[i]
                cur[i] = a + b
                a = a + b
    return


ways_init()
t = int(input())
for _ in range(t):
    n = int(input())
    print(cur[n] % MOD)

