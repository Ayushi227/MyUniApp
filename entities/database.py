import json
import os
from entities.student import Student
from entities.subject import Subject

class Database:
    DATABASE_FILE = "students.data"

    def __init__(self):
        if not os.path.exists(self.DATABASE_FILE):
            with open(self.DATABASE_FILE, 'w') as f:
                json.dump([], f)

    def read_all(self):
        try:
            with open(self.DATABASE_FILE, 'r') as f:
                data = json.load(f)
            students = []
            for s in data:
                student = Student(s['name'], s['email'], s['password'])
                student.id = s['id']
                for sub in s['subjects']:
                    subject = Subject()
                    subject.id = sub['id']
                    subject.mark = sub['mark']
                    subject.grade = sub['grade']
                    student.subjects.append(subject)
                students.append(student)
            return students
        except (json.JSONDecodeError, KeyError):
            print("Key error")
            return []

    def write_all(self, students):
        data = []
        for s in students:
            data.append({
                'id': s.id,
                'name': s.name,
                'email': s.email,
                'password': s.password,
                'subjects': [{'id': sub.id, 'mark': sub.mark, 'grade': sub.grade} for sub in s.subjects]
            })
        with open(self.DATABASE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def clear_all(self):
        with open(self.DATABASE_FILE, 'w') as f:
            json.dump([], f)

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
