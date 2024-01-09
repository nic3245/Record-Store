import pymysql
from crFunctions import *
from UDFunctions import *
from getby import *
import sys


def read_manager(conn):
    """Prompts the user to select a table to read and executes the corresponding function"""
    while True:
        print("What do you want to view?")
        print("1. Records")
        print("2. Record Players")
        print("3. Equipment")
        print("4. Records by Genre")
        print("5. Records by Artist")
        print("6. Schedule")
        print("7. Orders")
        print("8. Sections")
        print("9. Artists")
        print("10. Genres")
        print("11. Employees")
        print("12. Customers")
        choice = input("Enter the corresponding number: ")

        if choice == '1':
            e = get_all_records(conn)
            break
        elif choice == '2':
            e = get_all_record_players(conn)
            break
        elif choice == '3':
            e = get_all_equipment(conn)
            break
        elif choice == '4':
            e = get_records_by_genre(conn)
            break
        elif choice == '5':
            e = get_records_by_artist(conn)
            break
        elif choice == '6':
            e = get_schedule(conn)
            break
        elif choice == '7':
            e = get_orders(conn)
            break
        elif choice == '8':
            e = get_all_sections(conn)
            break
        elif choice == '9':
            e = get_all_artists(conn)
            break
        elif choice == '10':
            e = get_all_genres(conn)
            break
        elif choice == '11':
            e = get_all_employees(conn)
            break
        elif choice == '12':
            e = get_all_customers(conn)
            break
        else:
            print("Invalid choice. Please enter a valid number.")
    if e is not None:
        print("Error reading from the database:", e)


# Read function for employees

def read_employee(conn):
    """Prompts the user to select a table to read and executes the corresponding function"""
    while True:
        print("What do you want to view?")
        print("1. Records")
        print("2. Record Players")
        print("3. Equipment")
        print("4. Records by Genre")
        print("5. Records by Artist")
        print("6. Schedule")
        print("7. Orders")
        print("8. Sections")
        print("9. Artists")
        print("10. Genres")
        print("11. Customers")
        choice = input("Enter the corresponding number: ")
        if choice == '1':
            e = get_all_records(conn)
            break
        elif choice == '2':
            e = get_all_record_players(conn)
            break
        elif choice == '3':
            e = get_all_equipment(conn)
            break
        elif choice == '4':
            e = get_records_by_genre(conn)
            break
        elif choice == '5':
            e = get_records_by_artist(conn)
            break
        elif choice == '6':
            e = get_schedule(conn)
            break
        elif choice == '7':
            e = get_orders(conn)
            break
        elif choice == '8':
            e = get_all_sections(conn)
            break
        elif choice == '9':
            e = get_all_artists(conn)
            break
        elif choice == '10':
            e = get_all_genres(conn)
        elif choice == '11':
            e = get_all_customers(conn)
            break
        else:
            print("Invalid choice. Please enter a valid number.")

# Create function for managers


def create_manager(conn):
    """Prompts the user to select an entry to create and executes the corresponding function"""
    print("Which table would you like to create a new entry in?")
    print("1. Artist")
    print("2. Genre")
    print("3. Customer")
    print("4. Employee")
    print("5. Manager")
    print("6. Equipment")
    print("7. Record Player")
    print("8. Record")
    print("9. Order Item")
    print("10. Shift")
    print("11. Order")
    table_choice = input("Enter the corresponding number: ")

    if table_choice == "1":
        result = add_artist(conn)
        if result == 1:
            print("Artist added successfully.")
        else:
            print("Failed to add artist:", result)

    elif table_choice == "2":
        result = add_genre(conn)
        if result == 1:
            print("Genre added successfully.")
        else:
            print("Failed to add genre:", result)

    elif table_choice == "3":
        result = add_customer(conn)
        if isinstance(result[0][0], (int)):
            print("Customer added successfully.")
        else:
            print("Failed to add customer:", result)

    elif table_choice == "4":
        result = add_employee(conn)
        if result == 1:
            print("Employee added successfully.")
        else:
            print("Failed to add employee:", result)

    elif table_choice == "5":
        result = add_manager(conn)
        if result == 1:
            print("Manager added successfully.")
        else:
            print("Failed to add manager:", result)

    elif table_choice == "6":
        result = add_equipment(conn)
        if result == 1:
            print("Equipment added successfully.")
        else:
            print("Failed to add equipment:", result)

    elif table_choice == "7":
        result = add_record_player(conn)
        if result == 1:
            print("Record player added successfully.")
        else:
            print("Failed to add record player:", result)

    elif table_choice == "8":
        result = add_record(conn)
        if result == 1:
            print("Record added successfully.")
        else:
            print("Failed to add record:", result)

    elif table_choice == "9":
        result = add_order_item(conn)
        if result == 1:
            print("Order item added successfully.")
        else:
            print("Failed to add order item:", result)

    elif table_choice == "10":
        result = add_shift(conn)
        if result == 1:
            print("Shift added successfully.")
        else:
            print("Failed to add shift:", result)

    else:
        print("Invalid choice. Please enter a valid number.")

# Create function for employees


def create_employee(conn):
    """Prompts the user to select an entry to create and executes the corresponding function"""

    print("Which table would you like to create a new entry in?")
    print("1. Artist")
    print("2. Genre")
    print("3. Customer")
    print("4. Equipment")
    print("5. Record Player")
    print("6. Record")
    print("7. Order Item")
    table_choice = input("Enter the corresponding number: ")

    if table_choice == "1":
        result = add_artist(conn)
        if result == 1:
            print("Artist added successfully.")
        else:
            print("Failed to add artist:", result)

    elif table_choice == "2":
        result = add_genre(conn)
        if result == 1:
            print("Genre added successfully.")
        else:
            print("Failed to add genre:", result)

    elif table_choice == "3":
        result = add_customer(conn)
        if isinstance(result, (int)):
            print("Customer added successfully.")
        else:
            print("Failed to add customer:", result)

    elif table_choice == "4":
        result = add_equipment(conn)
        if result == 1:
            print("Equipment added successfully.")
        else:
            print("Failed to add equipment:", result)

    elif table_choice == "5":
        result = add_record_player(conn)
        if result == 1:
            print("Record player added successfully.")
        else:
            print("Failed to add record player:", result)

    elif table_choice == "6":
        result = add_record(conn)
        if result == 1:
            print("Record added successfully.")
        else:
            print("Failed to add record:", result)

    elif table_choice == "7":
        result = add_order_item(conn)
        if result == 1:
            print("Order item added successfully.")
        else:
            print("Failed to add order item:", result)

    else:
        print("Invalid choice. Please enter a valid number.")


# Update function for employees


# customer function


def customer(conn, customer_id):
    """Prompts the customer to select an option"""

    print("Welcome customer, what would you like to do ?")
    print("1. Make a new order")
    print("2. View your current and past orders.")
    print("3. Add an item to an order")
    print("4. View available records")
    print("5. View available players")
    print("6. View available equipment")
    print("7. Update your details")
    print("8. Exit the program")

    choice = input("Enter the corresponding number: ")

    if choice == "1":
        result = add_order(conn, customer_id, "Online")
        if result == 1:
            print("Order made successfully.")
        else:
            print("Failed to add order:", result)
    elif choice == "2":
        result = get_customer_orders(conn, customer_id)
        if result is not None:
            print("Error reading the database:", result)
    elif choice == "3":
        result = add_order_item(conn)
        if result == 1:
            print("Order item added successfully.")
        else:
            print("Failed to add order item:", result)

    elif choice == '4':
        records = get_all_records(conn)
        if records:
            print("Here are all the records in the database:")
            for record in records:
                print(record)
        else:
            print("Error retrieving records: ", records)

    elif choice == '5':
        record_players = get_all_record_players(conn)
        if record_players:
            print("Here are all the record players in the database:")
            for player in record_players:
                print(player)
        else:
            print("Error retrieving record players: ", record_players)

    elif choice == '6':
        equipment = get_all_equipment(conn)
        if equipment:
            print("Here are all the equipment in the database:")
            for item in equipment:
                print(item)
        else:
            print("Error retrieving equipment: ", equipment)
    elif choice == '7':
        e = update_customer_by_customer(conn, customer_id)
        if not e == 1:
            print("Error updating customer:", e)
    elif choice == "8":
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid number.")


# Emloyee function

def employee(conn):
    """Prompts the employee to choose between CRUD operations"""
    print("Welcome employee, what would you like to do?")
    print("1. Create a new entry")
    print("2. Read existing entries")
    print("3. Update existing entries")
    print("4. Delete existing entries")
    print("5. Exit the program.")
    choice = input("Enter the corresponding number: ")

    if choice == "1":
        create_employee(conn)
    elif choice == "2":
        read_employee(conn)
    elif choice == "3":
        # Nick put your update function for employees here
        update_employee_overall(conn)
    elif choice == "4":
        # Nick put your delete function for employees here
        delete_employee_overall(conn)
    elif choice == "5":
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid number.")


# Manager function

def manager(conn):
    """Prompts the manager to choose between CRUD operations"""
    print("Welcome manager, what would you like to do?")
    print("1. Create a new entry")
    print("2. Read existing entries")
    print("3. Update existing entries")
    print("4. Delete existing entries")
    print("5. Exit the program.")
    choice = input("Enter the corresponding number: ")

    if choice == "1":
        create_manager(conn)
    elif choice == "2":
        read_manager(conn)
    elif choice == "3":
        update_manager(conn)  # Nick put your update function for managers here
    elif choice == "4":
        delete_manager(conn)  # Nick put your delete function for managers here
    elif choice == "5":
        sys.exit()
    else:
        print("Invalid choice. Please enter a valid number.")

# Check manager function


def check_manager(conn, emp_id):
    """Checks if the employee with the given ID is a manager using a stored procedure"""
    try:
        cursor = conn.cursor()
        cursor.execute("CALL check_manager(%s)", (emp_id))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except pymysql.Error as err:
        return err
