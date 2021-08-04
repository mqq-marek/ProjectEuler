def fibonacci(a, b):
    yield a
    yield b
    i, j = a, b
    while True:
        i, j = j, i + j
        yield j


def fibonacci_words(a, b, n):
    al = len(a)
    bl = len(b)

    # Build lengths of each element of Fibonacci word sequence
    fib_len = []
    for f in fibonacci(al, bl):
        fib_len.append(f)
        if f >= n:
            break

    # Reverse back fibonacci lengths until find initial A or B word
    ndx = len(fib_len) - 1
    while ndx > 1:
        if fib_len[ndx - 2] < n:
            # if character in right side return back one time
            n -= fib_len[ndx] - fib_len[ndx - 1]
            ndx -= 1
        else:
            # else return back 2 times until part with offset in scope
            ndx -= 2
    if ndx == 0:
        return a[n - 1]
    else:
        return b[n - 1]


def hacker_main():
    q = int(input())
    for i in range(q):
        a, b, n = input().split()
        n = int(n)
        d = fibonacci_words(a, b, n)
        print(d)


def analyze_main():
    fb = []
    for w in fibonacci('A', 'B'):
        print(w)
        print(len(w), w.count('A'), w.count('B'))
        fb.append(w)
        if len(w) > 160:
            break


if __name__ == "__main__":
    hacker_main()
