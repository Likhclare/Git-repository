class Car:
    def drive(self):
        print("Driving")

class Plane:
    def fly(self):
        print("Flying")

class FlyingCar(Car, Plane):
    pass

fc = FlyingCar()
fc.drive()
fc.fly()
