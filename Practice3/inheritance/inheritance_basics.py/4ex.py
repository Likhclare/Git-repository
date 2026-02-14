class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def bark(self):
        print("Woof")

d = Dog()
d.speak()
d.bark()
#Inheritance allows us to define a class that inherits all the methods and properties from another class.