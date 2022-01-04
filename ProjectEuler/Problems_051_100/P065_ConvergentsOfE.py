"""

"""
from fractions import Fraction

def sqrt2_seq():
    yield 1
    while True:
        yield 2

def e_seq():
    start = 2
    yield start
    yield 1
    while True:
        yield start
        yield 1
        yield 1
        start *= 2

def fractions(seq):
    start = Fraction(next(seq))
    yield start
