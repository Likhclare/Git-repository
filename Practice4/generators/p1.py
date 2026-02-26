def square(n):
    for i in range(1,n + 1):
        yield i*i
r=square(7)
for i in r:
    print(i)