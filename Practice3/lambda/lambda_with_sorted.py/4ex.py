students = [("Ali", 85), ("Dana", 92), ("Omar", 78)]

result = sorted(students, key=lambda student: student[1])

print(result)
#The sorted() function can use a lambda as a key for custom sorting