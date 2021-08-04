import itertools
import math
import operator
from collections import Counter
from functools import reduce

DEBUG = False


def partitions(n):
    """
    Yields number n partitions.
    partitions(5) yields:
        [5]
        [1, 4]
        [2, 3]
        [1, 1, 3]
        [1, 2, 2]
        [1, 1, 1, 2]
        [1, 1, 1, 1, 1]
    """

    def next_partition():
        """
        Update partition to the next one with the same size.
        :return: True if next partition exist otherwise False
        """
        right_side_sum = 0
        for i in reversed(range(len(partition) - 1)):
            # Keep sum of elements skipped from right
            right_side_sum += partition[i + 1]
            # From the end look for the first element smaller than next
            if partition[i + 1] > partition[i]:
                # Borrow one
                partition[i+1] -= 1
                # Find next which is smaller for increasing them
                for j in reversed(range(i+1)):
                    if partition[j + 1] > partition[j]:
                        # Increase element j. Keep invariants that sum is n and numbers are monotonic
                        partition[j] += 1
                        # Now prepare for making minimal part on right of j
                        # all elements on right are equals partition[j] except last one which can be grater
                        right_j_sum = right_side_sum + (i - j) * partition[j+1]
                        distance = len(partition) - j - 2
                        for k in range(distance):
                            partition[j + k + 1] = partition[j]
                        partition[-1] = right_j_sum - distance * partition[j] - 1
                        return True
        # Not found any place for generating next partition with:
        #   - the same sum
        #   - the same length
        #   - having elements in order: partition[0] <= partition[1] .... <= partition[len(partition)-1]
        return False

    # Build partition length starting from 1 to n
    for m in range(n):
        partition = [1] * m
        partition.append(n - m)
        yield partition
        # Next partitions with the same size
        while next_partition():
            # assert all(a <= b for a, b in zip(partition, partition[1:])), partition
            # assert sum(partition) == n, partition
            yield partition


def nstr(n):
    if n < 10:
        return str(n)
    n -= 10
    if n < 26:
        return chr(ord('A') + n)
    n -= 26
    return chr(ord('a') + n)


def dynamic_level_loop(stop, *, start=None, step=None):
    def inc_overflow():
        pos = 0
        while True:
            if index[pos] + step[pos] < stop[pos]:
                index[pos] += step[pos]
                return False
            elif pos == len(index) - 1:
                return True
            else:
                index[pos] = start[pos]
                pos += 1

    stop = [s for s in stop]

    if start:
        start = [s for s in start]
    else:
        start = [0] * len(stop)

    index = [s for s in start]

    if step:
        step = [s for s in step]
    else:
        step = [1] * len(stop)

    if inc_overflow():
        return

    while True:
        yield index
        if inc_overflow():
            break


def n_xx_n_mod_k(n, k):
    """ Compute n ** n mod k. """
    return pow(n, n, k)


def n_xx_n_mod_k_frame(step, k):
    """ Build list size k with values: i ** i mod k, ...., (i + k -1) ** (i + k -1) mod k. """
    result = []
    for i in range(step * k, (step + 1) * k):
        result.append(n_xx_n_mod_k(i + 1, k))
    return result


def n_mod_k(n, k):
    """ Compute n mod k. """
    return (n * i) % k


def find_cycle(get_item, k, *, start=0, step=1):
    """ Find the shortest cycle of sequence build with get_item. """
    items = []
    for step in itertools.count(start=start, step=step):
        item = get_item(step, k)
        items.append(item)
        index = items.index(item)
        if index != len(items) - 1:
            break
    items.pop()
    return index, items


def flatten_list(items):
    for item in items:
        if isinstance(item, list):
            for sub_item in item:
                yield sub_item
        else:
            yield item


def n_xx_n_mod_k_cycle(k):
    """ Find the shortest cycle of sequence: 1 ** 1 mod k, 2 ** 2 mod k, ... """
    index, items = find_cycle(n_xx_n_mod_k_frame, k)

    elements = set(flatten_list(items))

    if DEBUG and False:
        print(f'n**n mod k: K={k}, elements={len(elements)}, cycle={len(items) - index}, start={index}')
        for item in items:
            print(item)
        print(elements)
    return index, items


def n_x_i_mod_k_cycle(n, k):
    """ Find the shortest cycle of sequence: 1 * n mod k, 2 * n mod k, ... """
    index, items = find_cycle(lambda i, j: i % j, k, start=n, step=n)
    assert index == 0
    assert items[-1] == 0
    items.pop()
    items.sort()
    if DEBUG and False:
        print(f'a*n mod k: K={k}, elements={len(items)}, cycle={len(items) - index}, start={index}')
        print(items)
    return index, items


def counts(n, k):
    index, items = n_xx_n_mod_k_cycle(k)
    cycle_size = (len(items) - index) * k
    offset = index * k
    elements = list(flatten_list(items))
    if len(elements) >= n:
        counter = Counter(elements[:n])
    else:
        cycles, reminder = divmod(n - offset, cycle_size)
        counter = Counter(elements[offset:])
        c_offset = Counter(elements[:offset])
        c_reminder = Counter(elements[offset:offset + reminder])
        for key in counter:
            counter[key] = cycles * counter[key] + c_offset[key] + c_reminder[key]
    k_cycle = {}
    for key in sorted(counter.keys()):
        if key:
            index, items = n_x_i_mod_k_cycle(key, k)
            k_cycle[key] = len(items)
    return counter, k_cycle


def find_sum(n, k):
    counter, cycle = counts(n, k)
    if DEBUG:
        print(f'Counter: {counter}')
        print(f'Cycle: {cycle}')
    cnt_counter = []
    cnt_values = []
    cycle[0] = 1
    for key in sorted(counter.keys()):
        if key or True:  # and cycle[key]:
            cnt_values.append(key)
            cnt_counter.append(min(counter[key], cycle[key]) + 1)
            # cnt_counter.append(cycle[key]+1)
    result = []
    if not cnt_counter:
        return None
    print(cnt_values)
    for v in dynamic_level_loop(cnt_counter):
        if math.gcd(*v) > 1:
            pass
            # continue
        dot = sum(map(operator.mul, v, cnt_values))
        if dot % k == 0:
            r = ''.join([nstr(p) * vv for vv, p in zip(v, cnt_values) if vv != 0])
            result.append(r)
    result.sort(key=lambda x: (len(x), x))
    len_cnt = Counter()
    for r in result:
        len_cnt[len(r)] += 1
    for key in sorted(len_cnt.keys()):
        print(key, len_cnt[key])
    for r in result:
        pass
        print(r)


L50 = sorted([n ** n % 50 for n in range(1, 11)])
L12 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def compute_l50():
    print(L50)
    cnt = 0
    for v in dynamic_level_loop([2, 2, 2, 2, 2, 2, 2, 2, 2, 2]):
        dot = sum(map(operator.mul, v, L50))
        if dot % 50 == 0:
            r = ''.join([nstr(i) for i in range(10) if v[i] != 0])
            print(cnt, r)
            cnt += 1


def compute_l12():
    print(L12)
    res = []
    for v in dynamic_level_loop([13, 7, 5, 4, 3, 3, 2, 2, 2, 2, 2, 2]):
        dot = sum(map(operator.mul, v, L12))
        if dot == 12:
            r = list(flatten_list([[L12[i]]*v[i] for i in range(len(L12)) if v[i] != 0]))
            res.append(r)

    res.sort(key=lambda x: (len(x), x))
    for r in res:
        print(r)
    print()


if __name__ == '__main__':
    DEBUG = True

    find_sum(10, 50)
    exit()
    for k in range(3, 20):
        for i in range(k * k + k, k * k + k + 1):
            print(f'I={i}, K={k}')
            find_sum(i, k)
            # counts(100, k)
