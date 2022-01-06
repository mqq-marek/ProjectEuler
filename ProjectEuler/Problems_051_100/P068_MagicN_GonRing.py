"""

Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.
....

"""
import itertools
from collections import defaultdict
from typing import Callable, Tuple, Iterator, Set, List

Numbers = Tuple[int, ...]
# Map triples with given sum based on second digit
triple_map = defaultdict(list)


def triple_digit_set(numbers: Numbers, triple_sum: int) -> Iterator[Numbers]:
    """Build possible triples with given sum."""
    for a, b, c in itertools.combinations(numbers, 3):
        if a + b + c == triple_sum:
            yield a, b, c
            yield a, c, b
            yield b, a, c
            yield b, c, a
            yield c, a, b
            yield c, b, a


def gong_generator(all_triples: List[Numbers], triples: List[Numbers], used_digits: Set[int], max_size, size):
    """
    Recursive gong generator.
    Start with the first triple which need to have minimum external (first) digit.
    Each next triple has unique external digit, second digit equal last digit of prev triple and
    unique last digit except last triple when last igit is equal second digit of the first triple.
    """
    start = triples[0][0]
    prev_last = triples[-1][2]
    # print(f'GongSet: {size}/{max_size}:{triples} {start}/{prev_last} {used_digits}')
    if size < max_size:
        for a, b, c in triple_map[prev_last]:
            if a > start and a not in used_digits and c not in used_digits:
                yield from gong_generator(all_triples, triples + [(a, b, c)], used_digits.union({a, b, c}), max_size, size + 1)
    else:
        for a, b, c in triple_map[prev_last]:
            if a > start and b == prev_last and c == triples[0][1] and a not in used_digits:
                yield triples + [(a, b, c)]


def triplets_to_str(num: Numbers) -> str:
    """Build string from triplet."""
    return ''.join(str(d) for d in num)


def solution_to_str(num: List[Numbers]) -> str:
    """Build string from triplet."""
    return ''.join(triplets_to_str(d) for d in num)


def gong_finder(n, s):
    numbers = tuple(i for i in range(1, 2 * n + 1))
    all_triples = sorted(triple_digit_set(numbers, s))
    for triple in all_triples:
        triple_map[triple[1]].append(triple)
    for triple in all_triples:
        if triple[0] <= n + 1:
            yield from gong_generator(all_triples, [triple], set(triple), n, 2)


def gong_solver(n, s):
    results = sorted(solution_to_str(solution) for solution in gong_finder(n, s))
    for str_triplets in results:
        print(''.join(str_triplets))


### Prev version with combinations/permutation - too slow
# def dial_digit_set(numbers: Numbers, size: int, condition: Callable[[Numbers], bool]) -> Iterator[Numbers]:
#     """Build possible inner dial sequences sequence set based on condition if applied."""
#     for dial in itertools.combinations(numbers, size):
#         if condition is None:
#             yield dial
#         elif condition(dial):
#             print(dial)
#             yield dial
#
#
# def dial_gent(numbers: Numbers) -> Iterator[Numbers]:
#     """Generate inner dial circle permutations form dial digit set. [One element fixed. (n-1)! possibilities]."""
#     for sub_dial in itertools.permutations(numbers[1:]):
#         dial = numbers[0], *sub_dial
#         yield dial
#
#
# def rotate_numbers(numbers: Iterator[Numbers]) -> Iterator[Numbers]:
#     """Rotate Numbers[triplets] until having as the first Number with the smallest digit."""
#     firsts = [num[0] for num in numbers]
#     min_num = min(firsts)
#     offset = firsts.index(min_num)
#     numbers = [numbers[(offset + ndx) % len(numbers)] for ndx in range(len(numbers))]
#     return numbers
#
#
# def triplets_to_str(num: Numbers) -> str:
#     """Build string from triplet."""
#     return ''.join(str(d) for d in num)
#
#
# def euler_triplets(dial: Numbers, ext_dials: Numbers, number_len: int) -> Iterator[str]:
#     """For project Euler final number need to have size characters."""
#     for ext_dial in itertools.permutations(ext_dials):
#         dial2 = *dial[1:], dial[0]
#         number = []
#         values = set()
#         for c, a, b in zip(ext_dial, dial, dial2):
#             num = c, a, b
#             values.add(a + b + c)
#             number.append(num)
#         if len(values) != 1:
#             # Not all triplets have the same digits sum
#             continue
#         number = rotate_numbers(number)
#         result = ''.join(triplets_to_str(t) for t in number)
#         if len(result) == number_len:
#             yield result
#
#
# def hacker_triplets(dial: Numbers, ext_dials: Numbers, triplet_sum: int) -> Iterator[str]:
#     """For Hackerrank final numbers need to have given sum """
#     dial2 = *dial[1:], dial[0]
#     number = []
#     values = set(ext_dials)
#     for a, b in zip(dial, dial2):
#         c = triplet_sum - a - b
#         if c not in values:
#             return
#         values.discard(c)
#         num = c, a, b
#         number.append(num)
#     # print(dial)
#     number = rotate_numbers(number)
#     result = ''.join(triplets_to_str(t) for t in number)
#     print(dial, result)
#     yield result
#
#
# def number_gen(n: int, s: int, dial_condition: Callable[[Numbers], bool],
#                triple_iter: Callable[[Numbers, Numbers, int], Iterator[str]]):
#     """Generate possible dial configurations and verify triplet conditions for being in result set."""
#     numbers = tuple(i for i in range(1, 2 * n + 1))
#     # Build available list of digits set for inner dial
#     for dials in dial_digit_set(numbers, n, dial_condition):
#         # Numbers not in inner dial
#         external_dial = tuple(i for i in numbers if i not in dials)
#         # Build every dial permutation based on dial digit set and find solution using triple iterator
#         for dial in dial_gent(dials):
#             yield from triple_iter(dial, external_dial, s)
#
#
# def euler_solver():
#     solutions = [number for number in number_gen(5, 16, lambda nums: True, euler_triplets)]
#     solutions = sorted(solutions)
#     for solution in solutions:
#         print(solution)
#
#
# def hacker_solver(n: int, s: int):
#     numbers = 2 * n
#     numbers_sum = numbers * (numbers + 1) // 2
#     inner_dial_sum = n * s - numbers_sum
#     solutions = [number for number in number_gen(n, s, lambda nums: sum(nums) == inner_dial_sum, hacker_triplets)]
#     solutions = sorted(solutions)
#     for solution in solutions:
#         print(solution)
#
#
# def show_min_max():
#     for n in range(3, 11):
#         numbers = tuple(i for i in range(1, 2 * n + 1))
#         sx1 = n * (n + 1) // 2
#         sx2 = n * (2 * n + 1)
#         min_sum = (sx2 + sx1) // n
#         max_sum = (sx2 + sx2 - sx1) // n
#         print(f"{n:2} sum min/max: {min_sum}/{max_sum}")
#         sum_list = []
#         for ss in range(min_sum, max_sum + 1):
#
#             # Build available list of digits set for inner dial
#             inner_dial_sum = n * ss - sx2
#             # for dials in dial_digit_set(numbers, n, lambda nums: sum(nums) == inner_dial_sum):
#             ssum = 0
#             for comb in itertools.combinations(numbers, 3):
#                 if sum(comb) == ss:
#                     ssum += 1
#             sum_list.append(ssum)
#         print(sum_list)


# euler_solver()
n, s = list(map(int, input().split()))
gong_solver(n, s)

