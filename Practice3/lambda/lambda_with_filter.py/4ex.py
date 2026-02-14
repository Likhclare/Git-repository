words = ["apple", "kiwi", "banana", "pear"]

result = list(filter(lambda word: len(word) > 4, words))

print(result)
#The filter() function creates a list of items for which a function returns True