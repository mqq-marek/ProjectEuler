import itertools
import math
import operator
from collections import Counter, defaultdict
from time import perf_counter

DEBUG = True
MODULO = 10 ** 9


def get_solution_by_iteration(n, k):
    for i, result in enumerate(scan_by_iteration(k), start=1):
        if i == n:
            return (result[0] - 1) % MODULO


def scan_by_iteration(k):
    """
    Yield solution using brute force method.
    For n we have 2**n all subsets divided into k bins [sum modulo k]
    Solution is bins[0] - 1 as empty set is not in scope.
    With step n+1 we increase amount of solution by 2**n having together 2**(n+1).
    New bins we compute in the following way: if (n+1)**(n+1) mod k is s then:
        we take amount of subsets in every bin and increase amount of solution in bin s elements further.
    """
    bins = [0] * k
    new_bins = [0] * k
    bins[0] = 1
    bins[1] = 1
    yield bins
    for i in itertools.count(2):
        s = pow(i, i, k)
        # for j in range(k):
        #     new_j = (j + s) % k
        #     new_bins[new_j] = (bins[j] + bins[new_j])  # % MODULO
        for j in range(k):
            new_bins[j] = (bins[j] + bins[j - s]) % MODULO
        bins, new_bins = new_bins, bins
        yield bins


def scan_by_iteration_2(k):
    """
    Yield solution using brute force method.
    For n we have 2**n all subsets divided into k bins [sum modulo k]
    Solution is bins[0] - 1 as empty set is not in scope.
    With step n+1 we increase amount of solution by 2**n having together 2**(n+1).
    New bins we compute in the following way: if (n+1)**(n+1) mod k is s then:
        we take amount of subsets in every bin and increase amount of solution in bin s elements further.
    """
    index, rem_list_of_items = find_cycle(n_xx_n_mod_k_frame, k)
    rem_items = list(flatten_list(rem_list_of_items))
    bins = [0] * k
    new_bins = [0] * k
    bins[0] = 1
    bins[1] = 1
    yield bins
    n_xx_n_mod_k_iter = itertools.chain(rem_items[:index], itertools.cycle(rem_items[index:]))
    next(n_xx_n_mod_k_iter)
    for s in n_xx_n_mod_k_iter:
        for j in range(k):
            new_bins[j] = bins[j] + bins[j - s]
        bins, new_bins = new_bins, bins
        yield bins


def scan_using_symbols(k, *, bins=None, start=1, end=None):
    """
    Yield solution using brute force but keeps results in symbolic forms.
    Every subset is represented as symbolic sum of initial state.
    So for example for k=3 we have initial state (the first step):
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    After 7 steps we have:
    [[20, 20, 24], [24, 20, 20], [20, 24, 20]]
    which means that the first subset has amount of:
        20 * initial amount of subset one plus
        20 * initial amount of subset two plus
        24 * initial amount of subset three

    """
    new_bins = [[]] * k
    for i in range(k):
        new_bins[i] = [0] * k

    if bins is None:
        bins = [[]] * k
        for i in range(k):
            bins[i] = [0] * k
            bins[i][i] = 1
            new_bins[i] = [0] * k
        if end and end < 1:
            return
        yield bins
        start += 1
    else:
        bins = bins[:]
    for i in itertools.count(start):
        if end and end < i:
            return
        s = pow(i, i, k)
        for j in range(k):
            new_bins[j] = [(old + new) % MODULO for old, new in zip(bins[j], bins[j - s])]
        bins, new_bins = new_bins, bins
        yield bins


def double_symbolic_element(elem):
    """
    Take symbolic representation and apply them to ourself, which result in doubling element.
    Having symbolic representation of element n give you symbolic representation of element 2*n + 1.
    Works for element n where n-1 is multiplication of k(exactly multiplication of cycle length which is is c*k).
    Algorithm works by applying result value to input value.
    """
    k = len(elem)
    res = [0] * k
    for e in range(k):
        res[e] = [sum(elem[e][j] * elem[j][i] for j in range(k)) % MODULO for i in range(k)]
    return res


def add_symbolic_elements(elem1, elem2):
    """ Add two symbolic representation. """
    k = len(elem1)
    res = [0] * k
    for e in range(k):
        res[e] = [sum(elem2[e][j]*elem1[j][i] for j in range(k)) % MODULO for i in range(k)]
    return res


def find_symbolic_cycle(k):
    values = []
    doubles = []
    symbolic_it = scan_using_symbols(k)
    next(symbolic_it)
    for ndx, element in enumerate(symbolic_it, start=2):
        # if ndx>250:
        #     break
        # if (ndx - 1) % k:
        #     continue
        values.append((ndx, element[:]))
        doubles.append(double_symbolic_element(element[:]))
        print(values[-1], '\n', doubles[-1])
        if element in doubles:
            dbl_index = doubles.index(element)
            index, value = values[dbl_index]
            # print(index, dbl_index, ndx)   #,  value[::-1], element[::-1])
            return index, ndx, value
        if ndx > 64:
            break


def find_symbolic_solution(n, k):
    #if k not in [16, 23, 24, 32, 40, 48]:
    base_ndx, dbl_ndx, base_value = find_symbolic_cycle(k)
    k_cycle = base_ndx - 1
    n_steps = (n - 1) // k_cycle
    manual_computing = n_steps * k_cycle + 2
    # print(f'cycle={k_cycle}, steps={n_steps}, manual={manual_computing},Base={base_value}')
    bins = [[]] * k
    for i in range(k):
        bins[i] = [0] * k
        bins[i][i] = 1
    while n_steps != 0:
        # print(f'steps={n_steps}, {bins}')
        if n_steps % 2:
            bins = add_symbolic_elements(bins, base_value)
        base_value = double_symbolic_element(base_value)
        n_steps //= 2
    # print(f'steps={n_steps}, {bins}')
    # print(f"manual from {manual_computing} to {n}")
    for ndx, element in enumerate(scan_using_symbols(k, bins=bins[:],
                                                     start=manual_computing, end=n), start=manual_computing):
        # print(f'Manual at {ndx}, {element}')
        bins = element[:]
    return bins


def get_solution(n, k):
    # test_value = get_solution_by_iteration(n, k)
    symbolic = find_symbolic_solution(n, k)
    # print(symbolic)
    result = (symbolic[0][0] + symbolic[0][1] - 1) % MODULO
    # if test_value != result:
    #     print('Results: ', n, k, test_value, result, symbolic)
    return result


def find_k_4(n):
    """Exact solution for k = 4."""
    if n == 1:
        return 1
    cycle, rem = divmod(n - 1, 4)
    adjustment = cycle * 3 - 1
    result = pow(2, n - 2) + pow(2, adjustment + rem)
    return result


def find_k_8(n):
    """Exact solution for k = 4"""
    if n == 1:
        return 1
    cycle, rem = divmod(n - 1, 4)
    adjustment = cycle * 3 - 2
    result = (pow(2, cycle * 4 - 2) + pow(2, adjustment)) * pow(2, rem)
    return result


def nstr(n):
    """Represent integer in radix with base up to 62 using digits, big letters and small letters. """
    if n < 10:
        return str(n)
    n -= 10
    if n < 26:
        return chr(ord('A') + n)
    n -= 26
    return chr(ord('a') + n)


def n_xx_n_mod_k(n, k):
    """ Compute n ** n mod k. """
    return pow(n, n, k)


def n_xx_n_mod_k_frame(step, k):
    """ Build list size k with values: i ** i mod k, ...., (i + k -1) ** (i + k -1) mod k. """
    result = []
    for i in range(step * k, (step + 1) * k):
        result.append(n_xx_n_mod_k(i + 1, k))
    return result


def find_cycle(get_item, k, *, start=0, step=1):
    """ Find the shortest cycle of sequence build with get_item. """
    items = []
    for offset in itertools.count(start=start, step=step):
        item = get_item(offset, k)
        items.append(item)
        index = items.index(item)
        if index != len(items) - 1:
            break
    items.pop()
    return index, items


def flatten_list(items):
    """Flatten two level lists into one level."""
    for item in items:
        if isinstance(item, list):
            yield from item
        else:
            yield item


def n_xx_n_mod_k_cycle(k):
    """ Find the shortest cycle of sequence: 1 ** 1 mod k, 2 ** 2 mod k, ... """
    index, items = find_cycle(n_xx_n_mod_k_frame, k)
    cycle_len = (len(items) - index) * k
    if DEBUG:
        print(
            f'K={k:2}, start={index:1}, cycle={len(items) - index:2}, start_len={index * k:2}, cycle_len={cycle_len:4}')
    return index, items


def view_main():
    x = 10**400
    for i in range(x, x+1):
        get_solution(i, 16)
    exit()
    for k in range(49, 51):
        tab = []
        log_k = int(math.log(k, 2))
        if k in {4, 8}:
            continue
        index, items = n_xx_n_mod_k_cycle(k)
        offset = index * k
        cycle_size = (len(items) - index) * k
        stop = 50  # * cycle_size + 2
        # it = find_using_symbols(k)
        find_symbolic_solution(100, k)
        continue
        for n, result in enumerate(scan_by_iteration(k), start=1):
            elem = next(it)
            next_d = double_symbolic_element(elem)
            print('Apply: ', n, elem, '->', next_d)
            if stop < n:
                break
            if (n - offset) % cycle_size == 0:
                tab.append(result[:])
    exit()


def euler_main():
    print(get_solution_by_iteration(250250, 250))


def hacker_main():
    n, k = [int(s) for s in input().split()]
    print(get_solution_by_iteration(n, k))


view_main()
