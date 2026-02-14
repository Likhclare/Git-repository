def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")
#If you do not know how many arguments will be passed into your function, add a * before the parameter name.