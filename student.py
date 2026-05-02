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
        return False

    def change_password(self, new_password):
        self.password = new_password

    def get_average_mark(self):
        if not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def is_passing(self):
        return self.get_average_mark() >= 50

    def get_overall_grade(self):
        avg = self.get_average_mark()
        if avg >= 85:
            return 'HD'
        elif avg >= 75:
            return 'D'
        elif avg >= 65:
            return 'C'
        elif avg >= 50:
            return 'P'
        else:
            return 'Z'

    def __str__(self):
        return f"{self.name} :: {self.id} --> Email: {self.email}"
