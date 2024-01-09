import pymysql
from UDFunctions import *
from crFunctions import *
from mecFuncs import *
import sys

# Main loop


def create_connection(user, password):
    """Create  MySQL connection"""
    conn = pymysql.connect(
        host='localhost',
        user=user,
        password=password,
        db='record_store',
        charset='utf8mb4'
    )
    return conn


def main():
    """Main loop"""
    while True:
        try:
            user = input("Enter your MySQL user: ")
            password = input("Enter your MySQL password: ")
            conn = create_connection(user, password)
            while True:
                print("What would you like to do?")
                print("1. Log in")
                print("2. Sign up")
                print("3. Exit the program")
                choice = input("Enter the corresponding number: ")

                if choice == "1":  # Log in
                    while True:
                        print("What is your role?")
                        print("1. Customer")
                        print("2. Employee")
                        user_role = input("Enter the corresponding number: ")

                        if user_role == "1":  # Customer
                            while True:
                                curr = conn.cursor()
                                query = "SELECT * FROM customer;"
                                curr.execute(query)
                                customer_ids = curr.fetchall()
                                c_id = int(input("Enter your customer ID: "))
                                if (c_id in customer for customer in customer_ids):
                                    while True:
                                        customer(conn, c_id)
                                else:
                                    print(
                                        "Not a valid customer ID. Contact our business if you forget your customer ID.")
                        elif user_role == "2":  # Employee
                            while True:
                                curr = conn.cursor()
                                query = "SELECT * FROM employee;"
                                curr.execute(query)
                                employee_ids = curr.fetchall()
                                emp_id = int(input("Enter your employee ID: "))
                                if (emp_id in emp for emp in employee_ids):
                                    if check_manager(conn, emp_id) == 1:
                                        while True:
                                            manager(conn)
                                    else:  # Regular employee
                                        while True:
                                            employee(conn)
                                else:
                                    print(
                                        "Not a valid employee ID. Contact your manager if you forget your employee ID.")
                        else:
                            print("Invalid choice. Please enter a valid number.")

                elif choice == "2":  # Sign up
                    print("Only customers can sign up.")
                    result = add_customer(conn)
                    if isinstance(result[0][0], (int)):
                        print(
                            "You've been added!. Here's your ID, don't forget it:", result[0][0])
                    else:
                        print("Failed to add customer:", result)
                elif choice == '3':
                    sys.exit()
                else:
                    print("Invalid choice. Please enter a valid number.")
        except pymysql.Error as err:
            print("Error logging in:", err)


if __name__ == "__main__":
    main()
