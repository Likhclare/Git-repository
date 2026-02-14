class Bird:
    def move(self):
        print("Flying")

class Penguin(Bird):
    def move(self):   # overriding
        print("Swimming")

p = Penguin()
p.move()
