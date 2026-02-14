class Student:
    def study(self):
        print("Studying")

class Athlete:
    def train(self):
        print("Training")

class StudentAthlete(Student, Athlete):
    pass

sa = StudentAthlete()
sa.study()
sa.train()
