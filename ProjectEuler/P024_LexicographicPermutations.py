"""

A permutation is an ordered arrangement of objects.
For example,  'dabc' is one possible permutation of the word 'abcd'.
If all of the permutations are listed alphabetically, we call it lexicographic order.
The lexicographic permutations of 'abc' are:
                  abc acb bac bca cab cba
What is the Nth lexicographic permutation of the word abcdefghijklm?

"""
import math

def permutation_number(s: str, num: int) -> str:
    """ Find Nth permutation of the string letters."""
    def nth(s, n):
        if n:
            n0, n1 = divmod(n, math.factorial(len(s)-1))
            s = s[n0] + nth(s[:n0]+s[n0+1:], n1)
        return s

    # Assume initial string is in lexicographic order
    assert all(a < b for a, b in zip(s, s[1:]))

    return nth(s, num-1)


if __name__ == "__main__":
    # print(permutation_number('0123456789', 1000000))
    word = 'abcdefghijklm'
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(permutation_number(word, n))
