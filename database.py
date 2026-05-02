import os
import pickle


class Database:
    DATABASE_FILE = "students.data"

    def __init__(self):
        if not os.path.exists(self.DATABASE_FILE):
            with open(self.DATABASE_FILE, 'wb') as f:
                pickle.dump([], f)

    def read_all(self):
        try:
            with open(self.DATABASE_FILE, 'rb') as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            return []

    def write_all(self, students):
        with open(self.DATABASE_FILE, 'wb') as f:
            pickle.dump(students, f)

    def clear_all(self):
        with open(self.DATABASE_FILE, 'wb') as f:
            pickle.dump([], f)

    def find_student_by_email(self, email):
        for student in self.read_all():
            if student.email == email:
                return student
        return None

    def find_student_by_id(self, student_id):
        for student in self.read_all():
            if student.id == student_id:
                return student
        return None

    def save_student(self, student):
        students = self.read_all()
        for i, s in enumerate(students):
            if s.id == student.id:
                students[i] = student
                self.write_all(students)
                return
        students.append(student)
        self.write_all(students)

    def delete_student(self, student_id):
        students = self.read_all()
        updated = [s for s in students if s.id != student_id]
        self.write_all(updated)
        return len(updated) < len(students)
