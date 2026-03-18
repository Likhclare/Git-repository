names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]
print("Индексы и имена:")
for i, name in enumerate(names):
    print(i, name)
print("\nИмена и оценки:")
for name, score in zip(names, scores):
    print(name, "=>", score)