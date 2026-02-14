class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):   # overriding
        print("Woof")

d = Dog()
d.speak()
