#  EER Model 

from datetime import date


class Person:
    def __init__(self, person_id, name, date_of_birth):
        self.person_id = person_id
        self.name = name
        self.date_of_birth = date_of_birth

    # Derived attribute
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )


class Staff(Person):
    def __init__(self, person_id, name, date_of_birth, employee_id, designation):
        super().__init__(person_id, name, date_of_birth)
        self.employee_id = employee_id
        self.designation = designation


class Member(Person):
    def __init__(self, person_id, name, date_of_birth, member_id):
        super().__init__(person_id, name, date_of_birth)
        self.member_id = member_id


class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author


class Loan:
    def __init__(self, loan_id, member, book, issue_date, return_date=None):
        self.loan_id = loan_id
        self.member = member
        self.book = book
        self.issue_date = issue_date
        self.return_date = return_date

    @property
    def is_returned(self):
        return self.return_date is not None