numbers = [2, -1, 3, -2, 4]
i = 0

while i < len(numbers):
    if numbers[i] < 0:
        i += 1
        continue
    print(numbers[i])
    i += 1
