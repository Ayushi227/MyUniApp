import re
from entities.student import Student
from entities.subject import Subject
from entities.database import Database
from colors import RED, GREEN, YELLOW, CYAN, RESET

EMAIL_PATTERN = re.compile(r'^[a-zA-Z]+\.[a-zA-Z]+@university\.com$')
PASSWORD_PATTERN = re.compile(r'^[A-Z][a-zA-Z]{5,}\d{3,}$')


def validate_credentials(email, password):
    return EMAIL_PATTERN.match(email) and PASSWORD_PATTERN.match(password)


class StudentController:
    def __init__(self):
        self.db = Database()

    def register(self):
        print(f"{GREEN}        Student Sign Up{RESET}")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not validate_credentials(email, password):
                print(f"{RED}        Incorrect email or password format{RESET}")
                continue

            print(f"{YELLOW}        email and password formats acceptable{RESET}")

            existing = self.db.find_student_by_email(email)
            if existing:
                print(f"{RED}        Student {existing.name} already exists{RESET}")
                return

            name = input("        Name: ").strip()
            student = Student(name, email, password)
            self.db.save_student(student)
            print(f"{YELLOW}        Enrolling Student {name}{RESET}")
            return

    def login(self):
        print(f"{GREEN}        Student Sign In{RESET}")
        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not validate_credentials(email, password):
                print(f"{RED}        Incorrect email or password format{RESET}")
                continue

            print(f"{YELLOW}        email and password formats acceptable{RESET}")

            student = self.db.find_student_by_email(email)
            if not student:
                print(f"{RED}        Student does not exist{RESET}")
                return

            if student.password != password:
                print(f"{RED}        Incorrect password{RESET}")
                return

            self.subject_menu(student)
            return

    def subject_menu(self, student):
        while True:
            choice = input(f"{CYAN}        Student Course Menu (c/e/r/s/x): {RESET}").strip().lower()

            if choice == 's':
                subjects = student.subjects
                print(f"{YELLOW}        Showing {len(subjects)} subjects{RESET}")
                for s in subjects:
                    print(f"        {s}")
            elif choice == 'e':
                if len(student.subjects) >= 4:
                    print(f"{RED}        Students are allowed to enrol in 4 subjects only{RESET}")
                    continue
                subject = Subject()
                print(f"{YELLOW}        Enrolling in Subject-{subject.id}{RESET}")
                student.enrol(subject)
                self.db.save_student(student)
                print(f"{YELLOW}        You are now enrolled in {len(student.subjects)} out of 4 subjects{RESET}")
            elif choice == 'r':
                subject_id = input("        Remove Subject by ID: ").strip()
                found = student.drop(subject_id)
                if found:
                    print(f"{YELLOW}        Droping Subject-{subject_id}{RESET}")
                    self.db.save_student(student)
                    print(f"{YELLOW}        You are now enrolled in {len(student.subjects)} out of 4 subjects{RESET}")
                else:
                    print(f"{RED}        Subject {subject_id} not found in enrolment{RESET}")
            elif choice == 'c':
                print(f"{YELLOW}        Updating Password{RESET}")
                new_pass = input("        New Password: ").strip()
                confirm = input("        Confirm Password: ").strip()
                while new_pass != confirm:
                    print(f"{RED}        Password does not match - try again{RESET}")
                    confirm = input("        Confirm Password: ").strip()
                student.change_password(new_pass)
                self.db.save_student(student)
            elif choice == 'x':
                break
            else:
                print(f"{RED}        Invalid option{RESET}")

    def student_menu(self):
        while True:
            choice = input(f"{CYAN}        Student System (l/r/x): {RESET}").strip().lower()

            if choice == 'r':
                self.register()
            elif choice == 'l':
                self.login()
            elif choice == 'x':
                break
            else:
                print(f"{RED}        Invalid option{RESET}")
