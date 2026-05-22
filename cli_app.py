from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
from colors import CYAN, YELLOW, RED, RESET


def main():
    student_ctrl = StudentController()
    admin_ctrl = AdminController()

    while True:
        choice = input(f"{CYAN}University System: (A)dmin, (S)tudent, or X : {RESET}").strip().upper()

        if choice == 'S':
            student_ctrl.student_menu()
        elif choice == 'A':
            admin_ctrl.admin_menu()
        elif choice == 'X':
            print(f"{YELLOW}Thank You{RESET}")
            break
        else:
            print(f"{RED}Invalid option{RESET}")


if __name__ == "__main__":
    main()
