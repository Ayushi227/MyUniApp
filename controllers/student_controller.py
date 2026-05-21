import re
from entities.student import Student
from entities.subject import Subject
from entities.database import Database

EMAIL_PATTERN = re.compile(r'^[a-zA-Z]+\.[a-zA-Z]+@university\.com$')
PASSWORD_PATTERN = re.compile(r'^[A-Z][a-zA-Z]{5,}\d{3,}$')


def validate_credentials(email, password):
    return EMAIL_PATTERN.match(email) and PASSWORD_PATTERN.match(password)


class StudentController:
    def __init__(self):
        self.db = Database()

    def register(self):
        print("        Student Sign Up")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not validate_credentials(email, password):
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            existing = self.db.find_student_by_email(email)
            if existing:
                print(f"        Student {existing.name} already exists")
                return

            name = input("        Name: ").strip()
            student = Student(name, email, password)
            self.db.save_student(student)
            print(f"        Enrolling Student {name}")
            return

    def login(self):
        print("        Student Sign In")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not validate_credentials(email, password):
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            student = self.db.find_student_by_email(email)
            if not student:
                print("        Student does not exist")
                return

            if student.password != password:
                print("        Incorrect password")
                return

            self.subject_menu(student)
            return

    def subject_menu(self, student):
        while True:
            choice = input("        Student Course Menu (c/e/r/s/x): ").strip().lower()

            if choice == 's':
                subjects = student.subjects
                print(f"        Showing {len(subjects)} subjects")
                for s in subjects:
                    print(f"        {s}")
            elif choice == 'e':
                if len(student.subjects) >= 4:
                    print("        Students are allowed to enrol in 4 subjects only")
                    continue
                subject = Subject()
                print(f"        Enrolling in Subject-{subject.id}")
                student.enrol(subject)
                self.db.save_student(student)
                print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")
            elif choice == 'r':
                subject_id = input("        Remove Subject by ID: ").strip()
                found = student.drop(subject_id)
                if found:
                    print(f"        Droping Subject-{subject_id}")
                    self.db.save_student(student)
                    print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")
                else:
                    print(f"        Subject {subject_id} not found in enrolment")
            elif choice == 'c':
                print("        Updating Password")
                new_pass = input("        New Password: ").strip()
                confirm = input("        Confirm Password: ").strip()
                while new_pass != confirm:
                    print("        Password does not match - try again")
                    confirm = input("        Confirm Password: ").strip()
                student.change_password(new_pass)
                self.db.save_student(student)
            elif choice == 'x':
                break
            else:
                print("        Invalid option")

    def student_menu(self):
        while True:
            choice = input("        Student System (l/r/x): ").strip().lower()

            if choice == 'r':
                self.register()
            elif choice == 'l':
                self.login()
            elif choice == 'x':
                break
            else:
                print("        Invalid option")
