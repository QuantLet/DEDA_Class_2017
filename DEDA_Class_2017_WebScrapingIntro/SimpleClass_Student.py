"""
Description:
 - Demonstrating how to create a class
 - Inheritance and Instantiation

Usage: Executing this whole file in your IDE or from Terminal or executing line by line in iPython.

Author: Junjie Hu, hujunjie@hu-berlin.de
Last modified date: 19-11-2017
"""


# Simple class


class Person(object):
    # The class Person is inherited from class object
    def __init__(self, first, last, gender, age):
        # self is the default argument that points to the instance
        # Using __init__ to initialize a class to take arguments
        self.first_name = first
        self.last_name = last
        self.gender = gender
        self.age = age


class Student(Person):
    # The class Student inherited from class Person
    def __init__(self, first, last, gender, age, school):
        # super() method allows us to handle the arguments from parent class without copying
        super().__init__(first, last, gender, age)
        # Child class can also be added new arguments
        self.school = school

    def describe(self):
        # describe is a method of class Student
        print('{0} {1} is a {2} years old {3} who studies at {4}.'.format(
            self.first_name,
            self.last_name,
            self.age,
            self.gender,
            self.school))


# stu_1 is an instance of class Student
stu_1 = Student('Jon', 'Doe', 'male', 10, 'C_School')
print("Is Student a subclass of Person: ", issubclass(Student, Person))
print("Is stu_1 an instance of Student: ", isinstance(stu_1, Student))
# Using the attributes in the object stu_1
print(stu_1.school)
# Using the methods in the object stu_1
stu_1.describe()
