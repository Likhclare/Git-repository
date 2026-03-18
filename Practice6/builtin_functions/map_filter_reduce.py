from functools import reduce
nums = [1, 2, 3, 4, 5, 6]
squared = list(map(lambda x: x**2, nums))
print(squared)
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)
total = reduce(lambda x, y: x + y, nums)
print(total)