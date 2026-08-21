# FUCTIONAL DEPENDENCY

students = [
    {"StudentID": 101, "StudentName": "Rahul", "Course": "CSE"},
    {"StudentID": 102, "StudentName": "Aman", "Course": "ECE"},
    {"StudentID": 103, "StudentName": "Vaseem", "Course": "CSE"},
]

# Check Functional Dependency:
# StudentID -> StudentName

fd_valid = True

for i in range(len(students)):
    for j in range(i + 1, len(students)):
        if students[i]["StudentID"] == students[j]["StudentID"]:
            if students[i]["StudentName"] != students[j]["StudentName"]:
                fd_valid = False

if fd_valid:
    print("StudentID -> StudentName is a Functional Dependency")
else:
    print("Functional Dependency is violated")