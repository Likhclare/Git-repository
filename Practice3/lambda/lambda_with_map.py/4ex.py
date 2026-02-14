list1 = [1, 2, 3]
list2 = [4, 5, 6]

result = list(map(lambda x, y: x + y, list1, list2))

print(result)
#The map() function applies a function to every item in an iterable