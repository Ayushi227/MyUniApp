from entities.database import Database


class AdminController:
    def __init__(self):
        self.db = Database()

    def show_students(self):
        students = self.db.read_all()
        print("        Student List")
        if not students:
            print("        < Nothing to Display >")
            return
        for s in students:
            print(f"        {s.name} :: {s.id} --> Email: {s.email}")

    def group_by_grade(self):
        students = self.db.read_all()
        print("        Grade Grouping")
        if not students:
            print("        < Nothing to Display >")
            return

        groups = {}
        for s in students:
            grade = s.get_overall_grade()
            if grade not in groups:
                groups[grade] = []
            groups[grade].append(s)

        for grade in sorted(groups.keys()):
            for s in groups[grade]:
                avg = s.get_average_mark()
                print(f"        {grade}  --> [{s.name} :: {s.id} --> GRADE: {grade:>2} - MARK: {avg:.2f}]")

    def partition_students(self):
        students = self.db.read_all()
        print("        PASS/FAIL Partition")

        passing = []
        failing = []
        for s in students:
            if s.is_passing():
                passing.append(s)
            else:
                failing.append(s)

        fail_str = ", ".join(
            f"{s.name} :: {s.id} --> GRADE: {s.get_overall_grade():>2} - MARK: {s.get_average_mark():.2f}"
            for s in failing
        )
        pass_str = ", ".join(
            f"{s.name} :: {s.id} --> GRADE: {s.get_overall_grade():>2} - MARK: {s.get_average_mark():.2f}"
            for s in passing
        )

        print(f"        FAIL --> [{fail_str}]")
        print(f"        PASS --> [{pass_str}]")

    def remove_student(self, student_id):
        found = self.db.delete_student(student_id)
        if found:
            print(f"        Removing Student {student_id} Account")
        else:
            print(f"        Student {student_id} does not exist")

    def clear_database(self):
        confirm = input("        Are you sure you want to clear the database (Y)ES/(N)O: ").strip()
        if confirm.upper() == 'Y':
            self.db.clear_all()
            print("        Students data cleared")

    def admin_menu(self):
        while True:
            choice = input("        Admin System (c/g/p/r/s/x): ").strip().lower()

            if choice == 's':
                self.show_students()
            elif choice == 'g':
                self.group_by_grade()
            elif choice == 'p':
                self.partition_students()
            elif choice == 'r':
                student_id = input("        Remove by ID: ").strip()
                self.remove_student(student_id)
            elif choice == 'c':
                print("        Clearing students database")
                self.clear_database()
            elif choice == 'x':
                break
            else:
                print("        Invalid option")
