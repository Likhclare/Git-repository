class Shape:
    def area(self):
        print("Area of shape")

class Circle(Shape):
    def area(self):   # overriding
        print("Area = πr²")

c = Circle()
c.area()
