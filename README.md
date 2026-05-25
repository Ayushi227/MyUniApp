# MyUniApp

A university enrolment system for UTS 32555 Fundamentals of Software Development — Assessment 1.
Built in Python with a CLI application (CLIUniApp) and a GUI application (GUIUniApp).

## Requirements

- Python 3.8 or higher
- tkinter (used for the GUI — included in the Python standard library)

No external packages need to be installed.

### Verify tkinter is available

```bash
python3 -m tkinter
```

A small test window should appear. If it doesn't, install tkinter:

```bash
# macOS (via Homebrew)
brew install python-tk

# Ubuntu / Debian
sudo apt-get install python3-tk
```

---

## How to Run

### Clone the repository

```bash
git clone https://github.com/Ayushi227/MyUniApp.git
cd MyUniApp
```

### Run the CLI app

```bash
python3 cli_app.py
```

### Run the GUI app

```bash
python3 gui_app.py
```

> Note: students must be registered via the CLI app first before they can log into the GUI.

---


## Project Structure

```
MyUniApp/
├── entities/
│   ├── student.py          # Student model class
│   ├── subject.py          # Subject model class
│   └── database.py         # File persistence (students.data)
├── controllers/
│   ├── student_controller.py   # Student system: register, login, subject enrolment menu
│   └── admin_controller.py     # Admin system: show, group, partition, remove, clear
├── cli_app.py              # CLIUniApp entry point
├── gui_app.py              # GUIUniApp entry point
├── students.data           # Auto-generated on first run (do not edit manually)
└── README.md
```

---

## How It Works

### CLIUniApp

On launch you are presented with the University System menu:

```
University System: (A)dmin, (S)tudent, or X :
```

**Student System** — register or log in as a student:
- Register with a valid email and password
- Enrol in up to 4 subjects (marks and grades are auto-generated)
- Remove a subject, view enrolments, or change password

**Admin System** — no login required:
- Show all students
- Group students by grade
- Partition students into PASS / FAIL
- Remove a student by ID
- Clear all student data

### GUIUniApp

A graphical interface for students only. Opens a login window and, after authenticating, gives access to:
- Enrol in subjects (up to 4)
- View enrolled subjects with marks and grades
- Remove individual subjects
- Error dialogs for invalid input or limit violations

---

## Credential Format

Credentials are validated against the following rules on both register and login:

| Field | Rule | Example |
|-------|------|---------|
| Email | `firstname.lastname@university.com` | `jane.doe@university.com` |
| Password | Starts with uppercase, 5+ letters, 3+ digits | `Hello123` |

---

## Data Persistence

All student data is stored in `students.data` using Python's `pickle` module. The file is created automatically on first run. Both the CLI and GUI apps read from and write to the same file, so changes made in one are reflected in the other.

---

## Grade Boundaries

| Mark Range | Grade |
|-----------|-------|
| 85 – 100 | HD (High Distinction) |
| 75 – 84 | D (Distinction) |
| 65 – 74 | C (Credit) |
| 50 – 64 | P (Pass) |
| 25 – 49 | Z (Fail) |

A student passes overall if their average mark across all enrolled subjects is 50 or above.
