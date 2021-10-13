"""

You are given around five-thousand first names, begin by sorting it into alphabetical order.
Then working out the alphabetical value for each name, multiply this value
by its alphabetical position in the list to obtain a name score.

"""
from collections import defaultdict

scores = {}


def process_names(names):
    names = sorted(names)
    for ndx, name in enumerate(names, 1):
        scores[name] = -ndx


def eval(name):
    score = scores[name]
    if score < 0:
        score *= -sum(ord(ch)-ord('@') for ch in name)
        scores[name] = score
    return score

def read_from_file(fn):
    names = []
    with open(fn) as f:
        for line in f.readlines():
            ns = line.split(',')
            ns = [n.replace('"', '') for n in ns]
            names.extend(ns)
    return names

def project_euler():
    ns = read_from_file('P022_Names.txt')
    ns.sort()
    print(ns[0], ns[937], ns[938], ns[-1])
    total = 0
    process_names(ns)
    for n in ns:
        total += eval(n)
    print(total)


if __name__ == "__main__":
    # project_euler()
    n = int(input())
    names = []
    for _ in range(n):
        names.append(input().strip())
    process_names(names)
    q = int(input())
    for _ in range(q):
        score = eval(input().strip())
        print(score)
