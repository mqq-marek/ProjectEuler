#!/bin/python3

import sys
import math

triangles = set()
maxt = set()
sqrt2 = math.sqrt(2)
s1 = 1 / (2 + sqrt2)
s2 = sqrt2 / (2 + sqrt2)


def triple2(n):
    global triangles
    product = -1
    base = (-1, -1, -1)
    for k in range(int(s2 * n), n // 2 + 1):
        kk = k * k
        for j in range (min((n-k) // 2, int(s1 * n)), max(n // 2, k)):
            if kk == j ** 2 + (n - k - j) ** 2:
                p = j * (n - j - k) * k
                m = math.gcd(j,  k, (n - j - k))
                b = (n - j - k)//m, j//m, k//m
                if b not in triangles:
                    triangles.add(base)
                    #print(f'New: {b} at {n}')
                if p > product:
                    product = p
                    base = b

    if product > 0:
        maxt.add(base)
        # print(f"Max: {base}")
    return product


def triple_product(n):
    pass


def hacker_main():
    t = int(input().strip())
    for a0 in range(t):
        n = int(input().strip())
        print(triple_product(n))


def ratio():
    minr = [1, 1, 1]
    maxr = [0, 0, 0]
    for t in maxt:
        s = sum(t)
        for i in range(3):
            maxr[i] = max(maxr[i], t[i]/s)
            minr[i] = min(minr[i], t[i]/s)
    print(f'Max ratio {maxr}')
    print(f'Min ratio {minr}')

def dev_main():
    for i in range(12, 2000):
        p = triple2(i)
    ratio()



if __name__ == '__main__':
    i = 1
    f = 1.6
    while f < 2 ** 100:
        f *= 1.6
        i += 1
    print(i)


    #dev_main()

