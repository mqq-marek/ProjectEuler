"""
The nth term of the sequence of triangle numbers is given by, tn =  n(n+1)/2; so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding
these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10.
If the word value is a triangle number then we shall call the word a triangle word.


"""
import math
from typing import Iterator


def word_value(word: str) -> int:
    return sum(ord(ch) - ord('A') + 1 for ch in word)


def file_words(file_name: str) -> Iterator[str]:
    with open(file_name, 'r') as file:
        for line in file:
            for word in line.split(','):
                if word[0] == '"' and word[-1] == '"':
                    yield word[1:-1]


def is_triangle(number: int) -> int:
    double = number + number
    n = int(math.sqrt(double))
    if n * (n + 1) == double:
        return n
    else:
        return -1


assert word_value('SKY') == 55


def project_euler_main():
    triangles = 0
    for index, word in enumerate(file_words('P042_Words.txt')):
        if is_triangle(word_value(word)) > 0:
            triangles += 1
    print(triangles)


#project_euler_main()
t = int(input())
for _ in range(t):
    tn = int(input())
    print(is_triangle(tn))