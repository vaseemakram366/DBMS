class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name


class Enrollment:
    def __init__(self, student, course):
        self.student = student
        self.course = course


# Create students
s1 = Student(1, "Vaseem", "vaseem@gmail.com")
s2 = Student(2, "Rahul", "rahul@gmail.com")

# Create courses
c1 = Course(101, "Python")
c2 = Course(102, "DBMS")

# Create relationships
e1 = Enrollment(s1, c1)
e2 = Enrollment(s1, c2)
e3 = Enrollment(s2, c1)

print(e1.student.name, "enrolled in", e1.course.course_name)
print(e2.student.name, "enrolled in", e2.course.course_name)
print(e3.student.name, "enrolled in", e3.course.course_name)