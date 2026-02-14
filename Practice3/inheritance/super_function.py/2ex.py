class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    self.graduationyear = 2019
#Python also has a super() function that will make the child class inherit all the methods and properties from its parent