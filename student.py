import random

class Student:
    def __init__(self, name, email, password):
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def enrol(self, subject):
        if len(self.subjects) >= 4:
            print("Students are allowed to enrol in 4 subjects only")
            return False
        for s in self.subjects:
            if s.id == subject.id:
                print(f"Already enrolled in subject {subject.id}")
                return False
        self.subjects.append(subject)
        return True

    def drop(self, subject_id):
        for s in self.subjects:
            if s.id == subject_id:
                self.subjects.remove(s)
                return True
        print(f"Subject {subject_id} not found in enrolment")
        return False

    def change_password(self, new_password):
        self.password = new_password

    def get_average_mark(self):
        if not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def is_passing(self):
        return self.get_average_mark() >= 50

    def __str__(self):
        return f"{self.name} :: {self.id} --> Email: {self.email}"
