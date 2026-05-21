import tkinter as tk
from entities.database import Database
from entities.subject import Subject
from controllers.student_controller import validate_credentials

DB = Database()


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent, message, title="Error"):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()

        self.configure(bg="#1e1e2e", padx=30, pady=20)

        icon_lbl = tk.Label(self, text="!", font=("Arial", 28, "bold"),
                            bg="#1e1e2e", fg="#f38ba8")
        icon_lbl.pack(pady=(0, 8))

        msg_lbl = tk.Label(self, text=message, font=("Arial", 11),
                           bg="#1e1e2e", fg="#cdd6f4",
                           wraplength=300, justify="center")
        msg_lbl.pack(pady=(0, 16))

        ok_btn = tk.Button(self, text="OK", width=10,
                           bg="#89b4fa", fg="#1e1e2e",
                           activebackground="#74c7ec",
                           font=("Arial", 10, "bold"),
                           relief="flat", cursor="hand2",
                           command=self.destroy)
        ok_btn.pack()

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


class SubjectWindow(tk.Toplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.student = student
        self.title(f"Enrolled Subjects - {student.name}")
        self.geometry("520x400")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self._build()

    def _build(self):
        tk.Label(self, text=f"Subjects for {self.student.name}",
                 font=("Arial", 14, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(20, 4))

        tk.Label(self, text=f"Enrolled in {len(self.student.subjects)} out of 4 subjects",
                 font=("Arial", 10), bg="#1e1e2e", fg="#a6e3a1").pack(pady=(0, 14))

        frame = tk.Frame(self, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=30)

        if not self.student.subjects:
            tk.Label(frame, text="No subjects enrolled yet.",
                     font=("Arial", 11), bg="#1e1e2e", fg="#6c7086").pack(pady=20)
        else:
            for s in self.student.subjects:
                row = tk.Frame(frame, bg="#313244", padx=12, pady=8)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=f"Subject::{s.id}",
                         font=("Arial", 11, "bold"),
                         bg="#313244", fg="#89dceb").pack(side="left")
                tk.Label(row, text=f"Mark: {s.mark}",
                         font=("Arial", 11),
                         bg="#313244", fg="#cdd6f4").pack(side="left", padx=16)
                grade_color = {'HD': '#a6e3a1', 'D': '#89b4fa',
                               'C': '#f9e2af', 'P': '#94e2d5', 'Z': '#f38ba8'}.get(s.grade, '#cdd6f4')
                tk.Label(row, text=f"Grade: {s.grade}",
                         font=("Arial", 11, "bold"),
                         bg="#313244", fg=grade_color).pack(side="left")

        avg = self.student.get_average_mark()
        status = "PASS" if self.student.is_passing() else "FAIL"
        status_color = "#a6e3a1" if status == "PASS" else "#f38ba8"

        footer = tk.Frame(self, bg="#1e1e2e")
        footer.pack(pady=14)
        tk.Label(footer, text=f"Average Mark: {avg:.2f}   Status: ",
                 font=("Arial", 11), bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        tk.Label(footer, text=status,
                 font=("Arial", 11, "bold"), bg="#1e1e2e", fg=status_color).pack(side="left")

        tk.Button(self, text="Close", command=self.destroy,
                  bg="#f38ba8", fg="#1e1e2e", font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2", width=10).pack(pady=(0, 16))


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.db = DB
        self.title("Subject Enrolment")
        self.geometry("480x440")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self._build()

    def _build(self):
        tk.Label(self, text="Subject Enrolment",
                 font=("Arial", 15, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(22, 2))

        self.name_lbl = tk.Label(self, text=f"Welcome, {self.student.name}",
                                 font=("Arial", 11),
                                 bg="#1e1e2e", fg="#a6e3a1")
        self.name_lbl.pack(pady=(0, 10))

        self.count_var = tk.StringVar()
        self._refresh_count()
        tk.Label(self, textvariable=self.count_var,
                 font=("Arial", 10),
                 bg="#1e1e2e", fg="#89b4fa").pack(pady=(0, 14))

        tk.Button(self, text="Enrol in a Subject",
                  command=self._enrol,
                  bg="#89b4fa", fg="#1e1e2e",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2", width=22, pady=6).pack(pady=6)

        tk.Button(self, text="View Enrolled Subjects",
                  command=self._view_subjects,
                  bg="#94e2d5", fg="#1e1e2e",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2", width=22, pady=6).pack(pady=6)

        tk.Button(self, text="Logout",
                  command=self.destroy,
                  bg="#f38ba8", fg="#1e1e2e",
                  font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2", width=14, pady=4).pack(pady=(18, 0))

    def _refresh_count(self):
        self.count_var.set(f"Enrolled in {len(self.student.subjects)} out of 4 subjects")

    def _enrol(self):
        if len(self.student.subjects) >= 4:
            ExceptionWindow(self,
                            "You are already enrolled in 4 subjects.\nThe maximum limit is 4 subjects.",
                            title="Enrolment Limit Reached")
            return
        subject = Subject()
        self.student.enrol(subject)
        self.db.save_student(self.student)
        self._refresh_count()
        ExceptionWindow(self,
                        f"Successfully enrolled in Subject-{subject.id}\n"
                        f"Mark: {subject.mark}  Grade: {subject.grade}",
                        title="Enrolled")

    def _view_subjects(self):
        SubjectWindow(self, self.student)


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUIUniApp - Student Login")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self.db = DB
        self._build()

    def _build(self):
        tk.Label(self, text="GUIUniApp",
                 font=("Arial", 20, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(30, 4))

        tk.Label(self, text="Student Login",
                 font=("Arial", 12),
                 bg="#1e1e2e", fg="#6c7086").pack(pady=(0, 20))

        form = tk.Frame(self, bg="#1e1e2e")
        form.pack(padx=40, fill="x")

        tk.Label(form, text="Email", font=("Arial", 10),
                 bg="#1e1e2e", fg="#cdd6f4", anchor="w").pack(fill="x")
        self.email_entry = tk.Entry(form, font=("Arial", 11),
                                    bg="#313244", fg="#cdd6f4",
                                    insertbackground="#cdd6f4",
                                    relief="flat", bd=6)
        self.email_entry.pack(fill="x", pady=(2, 12), ipady=4)

        tk.Label(form, text="Password", font=("Arial", 10),
                 bg="#1e1e2e", fg="#cdd6f4", anchor="w").pack(fill="x")
        self.pass_entry = tk.Entry(form, font=("Arial", 11),
                                    bg="#313244", fg="#cdd6f4",
                                    insertbackground="#cdd6f4",
                                    relief="flat", bd=6, show="*")
        self.pass_entry.pack(fill="x", pady=(2, 20), ipady=4)

        tk.Button(form, text="Login",
                  command=self._login,
                  bg="#89b4fa", fg="#1e1e2e",
                  font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2", pady=6).pack(fill="x")

        self.bind("<Return>", lambda e: self._login())

    def _login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not email or not password:
            ExceptionWindow(self, "Email and password fields cannot be empty.",
                            title="Missing Fields")
            return

        if not validate_credentials(email, password):
            ExceptionWindow(self,
                            "Incorrect email or password format.\n\n"
                            "Email must be: firstname.lastname@university.com\n"
                            "Password must start with uppercase, contain 5+ letters and 3+ digits.",
                            title="Format Error")
            return

        student = self.db.find_student_by_email(email)
        if not student:
            ExceptionWindow(self, "Student does not exist. Please register via the CLI app first.",
                            title="Student Not Found")
            return

        if student.password != password:
            ExceptionWindow(self, "Incorrect password.", title="Login Failed")
            return

        EnrolmentWindow(self, student)
        self.pass_entry.delete(0, tk.END)


def main():
    app = LoginWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
