"""
Triangle, pentagonal, and hexagonal numbers are generated by the following formulae:

Triangle	 	Tn=n(n+1)/2	 	1, 3, 6, 10, 15, ...
Pentagonal	 	Pn=n(3n−1)/2	 	1, 5, 12, 22, 35, ...
Hexagonal	 	Hn=n(2n−1)	 	1, 6, 15, 28, 45, ...
It can be verified that T285 = P165 = H143 = 40755.

Find the next triangle number that is also pentagonal and hexagonal.


For this challenge you are given , , , where  and
where  represents triangular numbers,  represents pentagonal numbers and  is hexagonal.
It can be observed that all hexagonal numbers are triangular numbers so we'll handle only 2 kinds of queries as
  , find all numbers below N which are Triangular number as well as Pentagonal
  , find all numbers below N which are Pentagonal number as well as Hexagonal

"""
import math


def revese_pentagonal(n):
    """
    Reverse pentagonal[1/6*(sqrt(24n+1)+1)].
    Return 0 for n < 0 or negate result is if is not positive integer result.
    """
    if n < 0:
        return 0
    delta = int(math.sqrt(1 + 24 * n))
    if delta * delta == 1 + 24 * n and delta % 6 == 5:
        return (delta + 1) // 6
    else:
        return - (delta + 1) // 6


def revese_triangle(n):
    """
    Reverse triangle [1/2*(sqrt(8n+1)-1)].
    Return 0 for n < 0 or negate result is if is not positive integer result.
    """
    if n < 0:
        return 0
    delta = int(math.sqrt(1 + 8 * n))
    if delta * delta == 1 + 8 * n and delta % 2 == 1:
        return (delta - 1) // 2
    else:
        return - (delta - 1) // 2


def revese_hexagonal(n):
    """
    Reverse hexagonal [1/4*(sqrt(8n+1)+1)].
    Return 0 for n < 0 or negate result is if is not positive integer result.
    """
    if n < 0:
        return 0
    delta = int(math.sqrt(1 + 8 * n))
    if delta * delta == 1 + 8 * n and delta % 4 == 3:
        return (delta + 1) // 4
    else:
        return - (delta + 1) // 4

