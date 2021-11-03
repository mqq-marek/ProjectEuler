import itertools
import math


DEBUG = True
MODULO = 10 ** 9

CYCLES = [(0, 6), (0, 4), (0, 20), (0, 6), (0, 42), (8, 8), (0, 18), (0, 20), (0, 110), (0, 12), (0, 156),
          (0, 42), (0, 60), (16, 16), (0, 272), (0, 18), (0, 342), (0, 20), (0, 42), (0, 110), (0, 506),
          (24, 24), (0, 100), (0, 156), (0, 54), (0, 84), (0, 812), (0, 60), (0, 930), (32, 32), (0, 330),
          (0, 272), (0, 420), (0, 36), (0, 1332), (0, 342), (0, 156), (40, 40), (0, 1640), (0, 42), (0, 1806),
          (0, 220), (0, 180), (0, 506), (0, 2162), (48, 48), (0, 294), (0, 100)]


def dbg_print(debug, *params):
    if debug:
        print(*params)


def get_solution_by_iteration(n, k):
    scan_iterator = scan_by_iteration(k)
    # scan_iterator = scan_by_iteration_2(k)
    for i, result in enumerate(scan_iterator, start=1):
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
    index, cycle, rem_items = find_cycle(k)
    bins = [0] * k
    new_bins = [0] * k
    bins[0] = 1
    bins[1] = 1
    yield bins
    rem_iter = itertools.chain(rem_items[:index], itertools.cycle(rem_items[index:]))
    next(rem_iter)
    for s in rem_iter:
        for j in range(k):
            new_bins[j] = bins[j] + bins[j - s]
        bins, new_bins = new_bins, bins
        yield bins


def init_bins(k):
    """
    Initialize bins for symbol computing.
    All 2**n subsets are divided into bins - each of them contains elements based on sum of elements mod k.
    Every variable representing amount of given bin elements can be represented as amount of other bins size
    from previous steps.
    Initially bin[0] is amount of bin[0] elements, .., bin[k-1] as elements of bin[k-1].
    Every iteration - going to next step modifies this state - see in scan_using_symbols.
    """
    bins = [0] * k
    bins[0] = 1
    return bins


def scan_using_symbols(k, *, bins=None, start=1):
    """
    Yield solution using brute force but keeps results in symbolic forms.
    Every subset is represented as symbolic sum of initial state.
    So for example for k=3 we have initial state (the first step):
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    After 7 steps we have:
    [[20, 20, 24], [24, 20, 20], [20, 24, 20], ...]
    which means that the first subset[mod k == 0] after 7 steps has amount of elements:
        20 * initial amount of subset one plus
        20 * initial amount of subset two plus
        24 * initial amount of subset three
    Note that every element is previous element rotation so you need to keep only the first.
    """
    if bins is None:
        bins = init_bins(k)
    else:
        bins = bins[:]

    yield bins

    for ndx in itertools.count(start + 1):
        s = pow(ndx, ndx, k)
        bins = [(bins[i] + bins[(i + s) % k]) % MODULO for i in range(k)]
        yield bins


def double_symbol(elem):
    """
    Take symbolic representation and apply them to ourself, which result in doubling element.
    Having symbolic representation of element n give you symbolic representation of element 2*n + 1.
    Works for element n where n-1 is multiplication of k(exactly multiplication of cycle length which is is c*k).
    Algorithm works by applying result value to input value.
    """
    return composite_symbols(elem, elem)


def composite_symbols(elem1, elem2):
    """ Add two symbolic representation."""
    k = len(elem1)
    # res = [[]] * k
    # for e in range(k):
    #     res[e] = [sum(elem2[e][j] * elem1[j][i] for j in range(k)) % MODULO for i in range(k)]
    res = [sum(elem1[i] * elem2[(k + j - i) % k]
               for i in range(k)) % MODULO
           for j in range(k)]
    # print(f'{res} = {elem1} * {elem2}')
    return res


def find_symbol_cycle(k):
    dbg = False
    values = []
    doubles = []
    offset, cycle, items = find_cycle(k)
    offset_k = offset * k
    start = offset_k + 1
    symbolic_it = scan_using_symbols(k, start=start)
    next(symbolic_it)
    counter = 0
    for ndx, element in enumerate(symbolic_it, start=start + 1):
        if (ndx - start) % k:
            continue
        counter += 1
        values.append((ndx, element[:]))
        doubles.append(double_symbol(element[:]))
        if element in doubles:
            dbl_index = doubles.index(element)
            index, value = values[dbl_index]
            cycle_k = ndx - index
            # print(k, offset_k, dbl_index, counter, index, ndx)
            # dbg_print(dbg, f'{k:2} - symbolic cycle len {cycle_k:4} from {index - cycle_k + 1:2} to {index:4} '
            #                f'doubles at index {ndx:4}, offset={offset_k}')
            return offset_k, index - offset_k - 1, value


def find_symbolic_solution_old(n, k):
    dbg = False

    prefix, k_cycle = CYCLES[k-3]
    dbg_print(dbg, f'Find n={n}, k={k}, prefix={prefix}, cycle={k_cycle}')
    n_steps = max(0, (n - 1 - prefix) // k_cycle)
    n_rem_len = max(0, n - prefix - n_steps * k_cycle)
    end_cycle_ndx = prefix + k_cycle + 1

    for ndx, base_value in enumerate(scan_using_symbols(k, start=prefix+1), start=prefix+1):
        if ndx == end_cycle_ndx:
            break

    # offset, base_ndx, dbl_ndx, base_value = find_symbol_cycle(k)

    n_steps = max(0, (n - 1 - prefix) // k_cycle)
    ending_start = prefix + n_steps * k_cycle + 1
    dbg_print(dbg, f'cycle={k_cycle}, steps={n_steps}, manual={ending_start},Base={base_value}')

    for ndx, element in enumerate(scan_using_symbols(k), start=1):
        bins = element[:]
        if ndx == n or ndx == prefix + 1:
            break

    while n_steps != 0:
        dbg_print(dbg, f'steps={n_steps}, {bins}')
        if n_steps % 2:
            bins = composite_symbols(bins, base_value)
        base_value = double_symbol(base_value)
        n_steps //= 2
    dbg_print(dbg, f'steps={n_steps}, {bins}')
    for ndx, element in enumerate(scan_using_symbols(k, bins=bins[:], start=ending_start), start=ending_start):
        if ndx > n:
            break
        # dbg_print(dbg, f'Manual at {ndx}, {element}')
        bins = element[:]
        dbg_print(dbg, f'final={bins}')
    return bins


def find_symbolic_solution(n, k):
    """
    Find solution using symbolic computation.
    Computation for n is divided into 3 parts:
        - Compute prefix value [some k has prefix values which are not part of cycles]
        - Compute cycle part [amount of cycles = (n - prefix) // cycle_size
        - Compute remainder part = n - offset - (n - prefix) // cycle_size
    """
    dbg = False

    #
    # prefix, base_ndx, dbl_ndx, base_value = find_symbol_cycle(k)

    prefix, k_cycle = CYCLES[k-3]
    dbg_print(dbg, f'Find n={n}, k={k}, prefix={prefix}, cycle={k_cycle}')

    n_steps = max(0, (n - 1 - prefix) // k_cycle)
    n_rem_len = max(0, n - prefix - n_steps * k_cycle)
    end_cycle_ndx = k_cycle + 1

    rem_value = init_bins(k)
    for ndx, base_value in enumerate(scan_using_symbols(k, start=prefix + 1), start=1):
        dbg_print(dbg, base_value)
        if ndx == n_rem_len:
            rem_value = base_value[:]
            dbg_print(dbg, f'rem_ndx={n_rem_len}, {rem_value}')
        if ndx == end_cycle_ndx:
            dbg_print(dbg, f'base={base_value}')
            break

    dbg_print(dbg, f'cycle={k_cycle}, steps={n_steps}, manual={n_rem_len-1}, Base={base_value}')

    for ndx, element in enumerate(scan_using_symbols(k), start=1):
        bins = element[:]
        if ndx == n or ndx == prefix + 1:
            break

    while n_steps != 0:
        dbg_print(dbg, f'steps={n_steps}, {bins}')
        if n_steps % 2:
            bins = composite_symbols(bins, base_value)
        base_value = double_symbol(base_value)
        n_steps //= 2
    dbg_print(dbg, f'steps={n_steps}, {bins}')
    if n_rem_len > 1:
        bins = composite_symbols(rem_value, bins)
    dbg_print(dbg, f'final={bins}')
    # for ndx, element in enumerate(scan_using_symbols(k, bins=bins[:], start=ending_start), start=ending_start):
    #     if ndx > n:
    #         break
    #     # dbg_print(dbg, f'Manual at {ndx}, {element}')
    #     bins = element[:]
    return bins


def get_solution(n, k):
    symbolic = find_symbolic_solution(n, k)
    result = (symbolic[0] + symbolic[1] - 1) % MODULO
    return result


def verify_solution(n, k):
    test_value = get_solution_by_iteration(n, k)
    symbolic = find_symbolic_solution(n, k)
    # print(symbolic)
    result = (symbolic[0] + symbolic[1] - 1) % MODULO
    if test_value != result:
        print('Results: ', n, k, test_value, result, symbolic)
        assert False
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


def find_cycle(k, *, start=0, step=1):
    """ Find the shortest cycle of sequence division remainder with optionally itial offset if not zero. """
    items = []
    for i in itertools.count(start=start, step=step):
        item = n_xx_n_mod_k_frame(i, k)
        items.append(item)
        prefix = items.index(item)
        if prefix != len(items) - 1:
            break
    items.pop()
    cycle = len(items) - prefix
    return prefix, cycle, list(flatten_list(items))


def flatten_list(items):
    """Flatten two level lists into one level."""
    for item in items:
        if isinstance(item, list):
            yield from item
        else:
            yield item


def view_main():
    k = 8
    for k in range(3, 51):
        for i in range(1, 100):
            verify_solution(i, k)
    exit()
    for k in range(25, 26):
        tab = []
        log_k = int(math.log(k, 2))
        if k in {4, 8}:
            continue
        index, items = find_cycle(k)
        offset = index * k
        cycle_size = (len(items) - index) * k
        stop = 50  # * cycle_size + 2
        # it = find_using_symbols(k)
        find_symbolic_solution(100, k)
        continue
        for n, result in enumerate(scan_by_iteration(k), start=1):
            elem = next(it)
            next_d = double_symbol(elem)
            print('Apply: ', n, elem, '->', next_d)
            if stop < n:
                break
            if (n - offset) % cycle_size == 0:
                tab.append(result[:])
    exit()


def cycle_main():
    """Build cycle table."""
    symbol_cycle_tab = []
    for k in range(3, 51):
        prefix, cycle, rem_items = find_cycle(k)
        cycle_k = cycle * k
        prefix_k = prefix * k
        prefix_s, cycle_s, value = find_symbol_cycle(k)
        symbol_cycle_tab.append((prefix_s, cycle_k))
        if DEBUG:
            print(
                f'K={k:2}, prefix={prefix:1}/{prefix_k:2}, r_cycle={cycle:2}/{cycle_k:4}, '
                f' prefix_sym={prefix_k:2}, cycle_sym={cycle_s:4}, rem/sym ratio={cycle_k // cycle_s}')
            # if prefix:
            #     print(f'Prefix_value: {rem_items[:prefix_k]}')
            # print(f'Cycle_value: {rem_items[prefix_k:]}')
    # with open('cycle.txt', 'w') as f:
    #     print(repr(symbol_cycle_tab), file=f)
    print(symbol_cycle_tab)


def euler_main():
    print(get_solution_by_iteration(250250, 250))


def hacker_main():
    n, k = [int(s) for s in input().split()]
    print(get_solution(n, k))


# euler_main()
# hacker_main()
# view_main()
# cycle_main()
# symbolic_main()


for k in range(3, 50):
    for n in range(1, 20):
        verify_solution(n, k)

