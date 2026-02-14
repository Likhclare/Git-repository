class Employee:
    def work(self):
        print("Working")

class Manager(Employee):
    def work(self):   # overriding
        print("Managing team")

m = Manager()
m.work()
