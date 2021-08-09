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

seq = [0] * (5 * 10 ** 6 + 2)
seq[2] = 1
first_len = [(2, 1)]

def collatz(n):
    if n < 2:
        return 0
    if n < len(seq) and seq[n]:
        return seq[n]
    count = 0
    visited = []
    while True:
        visited.append(n)
        count += 1
        if n % 2:
            n = 3 * n + 1
        else:
            n = n // 2
        if n < len(seq) and seq[n]:
            for i, j in enumerate(visited[::-1], 1):
                if j < len(seq):
                    seq[j] = seq[n] + i
            return seq[n] + count


def longest_up_to(n):
    longest = 0
    longest_pos = 1

    for i, (pos, seq_len) in enumerate(first_len):
        if pos <= n:
            longest = seq_len
            longest_pos = pos
        else:
            break

    for i in range(longest_pos + 1, n + 1):
        seq_len = collatz(i)
        if seq_len > longest:
            first_len.append((i, seq_len))
        if seq_len >= longest:
            longest = seq_len
            longest_pos = i
    return longest_pos


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        seq_pos = longest_up_to(n)
        print(seq_pos)


def dev_main():
    seq_pos = longest_up_to(1000000)

    print(seq_pos, seq[seq_pos-2:seq_pos+3])


dev_main()