words = ["apple", "kiwi", "banana", "pear"]

result = sorted(words, key=lambda word: len(word))

print(result)
#The sorted() function can use a lambda as a key for custom sorting