# object oriented

from datetime import date


class Person:
    def __init__(self, person_id, name, date_of_birth):
        self._person_id = person_id
        self._name = name
        self._date_of_birth = date_of_birth

    # Encapsulation
    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return self._name

    # Derived attribute
    @property
    def age(self):
        today = date.today()
        return today.year - self._date_of_birth.year - (
            (today.month, today.day)
            < (self._date_of_birth.month, self._date_of_birth.day)
        )

    def display_info(self):
        return f"ID: {self._person_id}, Name: {self._name}, Age: {self.age}"


class Member(Person):
    def __init__(self, person_id, name, date_of_birth, member_id):
        super().__init__(person_id, name, date_of_birth)
        self._member_id = member_id
        self._loans = []

    def borrow_book(self, book):
        loan = Loan(self, book)
        self._loans.append(loan)
        book.issue()

    def return_book(self, book):
        for loan in self._loans:
            if loan.book == book and not loan.returned:
                loan.return_book()
                break


class Staff(Person):
    def __init__(
        self,
        person_id,
        name,
        date_of_birth,
        employee_id,
        designation
    ):
        super().__init__(person_id, name, date_of_birth)
        self._employee_id = employee_id
        self._designation = designation

    def approve_loan(self, loan):
        loan.approve(self)


class Book:
    def __init__(self, book_id, title, author):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._available = True

    @property
    def title(self):
        return self._title

    @property
    def available(self):
        return self._available

    def issue(self):
        if not self._available:
            raise ValueError("Book is already issued.")

        self._available = False

    def return_book(self):
        self._available = True


class Loan:
    def __init__(self, member, book):
        self._member = member
        self._book = book
        self._issue_date = date.today()
        self._return_date = None
        self._approved_by = None

    @property
    def book(self):
        return self._book

    @property
    def returned(self):
        return self._return_date is not None

    def approve(self, staff):
        self._approved_by = staff

    def return_book(self):
        self._return_date = date.today()
        self._book.return_book()


# -----------------------------
# OBJECT CREATION
# -----------------------------

member = Member(
    person_id=101,
    name="Vaseem",
    date_of_birth=date(2007, 1, 7),
    member_id="M101"
)

staff = Staff(
    person_id=201,
    name="Library Staff",
    date_of_birth=date(1990, 5, 10),
    employee_id="E201",
    designation="Librarian"
)

book = Book(
    book_id="B101",
    title="The Elements of Computing Systems",
    author="Nisan and Schocken"
)

# Member borrows book
member.borrow_book(book)

# Staff approves the loan
loan = member._loans[0]
staff.approve_loan(loan)

print(member.display_info())
print(book.title)
print(book.available)

# Member returns book
member.return_book(book)

print(book.available)