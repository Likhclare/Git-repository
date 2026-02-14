class Counter:
    count = 0   # class variable

    def __init__(self):
        Counter.count += 1

a = Counter()
b = Counter()
print(Counter.count)  # 2
