"""

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome.
A number that never forms a palindrome through the reverse and add process is called a Lychrel number.
ue to the theoretical nature of these numbers, and for the purpose of this problem,
we shall assume that a number is Lychrel until proven otherwise.
In addition you are given that for every number below ten-thousand, it will either
(i) become a palindrome in less than fifty iterations (60 for HackerRank!!!!!!), or,
(ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome.
In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome:
4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

[Euler] How many Lychrel numbers are there below ten-thousand?
[Hacker] Given N, find the palindrome to which maximum numbers in range [1, n] converge.
Print the palindrome and the count.


"""
from collections import defaultdict


def is_palindrome(n: int) -> bool:
    n_as_str = str(n)
    return n_as_str == n_as_str[::-1]


def is_not_lychrel(n: int, max_iter: int = 59) -> int:
    if is_palindrome(n):
        return n
    for _ in range(1, max_iter + 1):
        n = n + int(str(n)[::-1])
        if is_palindrome(n):
            return n
    return 0


def euler_main():
    counter = 0
    for i in range(1, 10000):
        if not is_not_lychrel(i, max_iter=50):
            counter += 1
    print(counter)


def hacker_main():
    n = int(input())
    counter = defaultdict(int)
    for i in range(1, n + 1):
        palindrome = is_not_lychrel(i)
        if palindrome:
            counter[palindrome] += 1
    frequency = 0
    palindrome = 0
    for key, value in counter.items():
        if value >= frequency:
            frequency = value
            palindrome = key
    print(palindrome, frequency)


# euler_main()
hacker_main()