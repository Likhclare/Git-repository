def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")
#If you do not know how many arguments will be passed into your function, add a * before the parameter name.