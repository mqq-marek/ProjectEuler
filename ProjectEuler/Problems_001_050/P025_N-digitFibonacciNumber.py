"""

The Fibonacci sequence is defined by the recurrence relation: F(n) = F(n-1) + F(n-2), F(1) = 1, F2(0) = 1

What is the first term in the Fibonacci sequence to contain Nth digits?

"""
from itertools import takewhile

MAX_DIGITS = 5001
fibonacci_index = [0] * (MAX_DIGITS + 1)


def fibonacci():
    """
    Fibonacci numbers generator.
    :yields: fibonacci sequence: 0, 1, 1, 2, 3, 5
    """
    f_current: int = 0
    f_next: int = 1
    while True:
        yield f_current
        f_current, f_next = f_next, f_current + f_next


def counter(condition, iterable):
    it_counter = 1
    for i in iterable:
        if condition(i):
            return it_counter
        it_counter += 1


def fibonacci_first_with_n_digits(n):
    num = 10 ** n
    # return sum(1 for i in takewhile(lambda f: len(str(f)) < n, fibonacci()))
    return sum(1 for i in takewhile(lambda f: f < num, fibonacci()))


def init():
    next_len = 1
    next_power = 1
    for ndx, fib in enumerate(fibonacci(), 0):
        if next_len > MAX_DIGITS:
            break
        if fib > next_power and fibonacci_index[next_len] == 0:
            fibonacci_index[next_len] = ndx
            next_len += 1
            next_power *= 10


init()
# print(fibonacci_first_with_n_digits(1000))
t = int(input())
for _ in range(t):
    n = int(input())
    print(fibonacci_index[n])