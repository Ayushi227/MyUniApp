from student_controller import StudentController
from admin_controller import AdminController


def main():
    student_ctrl = StudentController()
    admin_ctrl = AdminController()

    while True:
        choice = input("University System: (A)dmin, (S)tudent, or X : ").strip().upper()

        if choice == 'S':
            student_ctrl.student_menu()
        elif choice == 'A':
            admin_ctrl.admin_menu()
        elif choice == 'X':
            print("Thank You")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
