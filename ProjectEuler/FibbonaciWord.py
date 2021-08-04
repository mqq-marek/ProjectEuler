

def Fibbonacii(a, b):
    yield a
    yield b
    i, j = a, b
    while True:
        i, j = j, i + j
        yield j


def fibb_char(a, b, n):
    al = len(a)
    bl = len(b)
    fib_len = []
    for f in Fibbonacii(al, bl):
        fib_len.append(f)
        if f >= n:
            break
    ndx = len(fib_len-1)
    while ndx > 1:
        n -= fib_len[ndx-2]
        ndx -= 1
    if ndx == 0:
        return a[n-1]
    else:
        return b[n-1]




def hacker_main():
    q = int(input())
    for i in range(q):
        a, b, n = input().split()
        n = int(n)
        d = fibb_char(a, b, n)
        print(d)

def dev_main():


fb = []
for w in Fibbonacii('A', 'B'):
    print(w)
    print(len(w), w.count('A'), w.count('B'))
    fb.append(w)
    if len(fb) > 5:
        w = fb[-3] + fb[-4] + fb[-3]
        #print(f'-{w}')
    if len(w) > 160:
        break