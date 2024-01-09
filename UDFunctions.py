import pymysql
from crFunctions import get_all_records, get_all_record_players, get_all_equipment, get_orders, get_schedule, get_all_employees, get_all_sections, get_all_artists, get_all_customers, get_all_genres


def choose_order(conn):
    curr = conn.cursor()
    curr.callproc("view_all_orders", ())
    orders = curr.fetchall()
    while True:
        try:
            id_to_update = input(
                "Which order id would you like to select? Input v to see orders: ")
            if id_to_update == "v" or id_to_update == "V":
                e = get_orders(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            if any(int(id_to_update) in order for order in orders):
                break
            else:
                print("Id does not exist")
        except:
            print("Please enter a valid id.")
    return next(order for order in orders if order[0] == int(id_to_update))


def choose_order_item(conn, order):
    while True:
        try:
            id_to_update = input(
                "What item id would you like select based on your order? Input v to see items: ")
            if id_to_update == "v" or id_to_update == "V":
                for item in order:
                    print(item)
            if any(int(id_to_update) in item for item in order):
                break
            else:
                print("Id not in order, try again.")
        except:
            print("Please enter a valid id.")
    return next(item for item in order if item[0] == int(id_to_update))


def choose_record(conn):
    """has user choose a record and returns it as a tuple"""
    # choose record to change
    curr = conn.cursor()
    curr.callproc("view_all_records", ())
    records = curr.fetchall()
    while True:
        try:
            id_to_update = input(
                "Which record id would you like to select? Input v to see records: ")
            if id_to_update == "v" or id_to_update == "V":
                e = get_all_records(conn)
                if e is not None:
                    print("Error reading from the database:", e)
                id_to_update = input("Please choose an id from the list")
            if any(int(id_to_update) in record for record in records):
                break
            else:
                print("Id does not exist")
        except:
            print("Please enter a valid id.")
    return next(record for record in records if record[0] == int(id_to_update))


def choose_record_player(conn):
    """has user choose a record player and returns it as a tuple"""
    # choose record player to change
    curr = conn.cursor()
    curr.callproc("view_all_recordplayers", ())
    records = curr.fetchall()
    while True:
        try:
            id_to_update = input(
                "Which record player id would you like to select? Input v to see record players: ")
            if id_to_update == "v" or id_to_update == "V":
                e = get_all_record_players(conn)
                if e is not None:
                    print("Error reading from the database:", e)
                id_to_update = input("Please choose an id from the list")
            if any(int(id_to_update) in record for record in records):
                break
            else:
                print("Id does not exist")
        except:
            print("Please enter a valid id.")
    return next(record for record in records if record[0] == int(id_to_update))


def choose_equipment(conn):
    """has user choose an equipment and returns it as a tuple"""
    # choose equipment to change
    curr = conn.cursor()
    curr.callproc("view_all_equipment", ())
    equipment = curr.fetchall()
    while True:
        try:
            equipment_to_update = input(
                "Which equipment id would you like to select? Input v to see equipment: ")
            if equipment_to_update == "v" or equipment_to_update == "V":
                e = get_all_equipment(conn)
                if e is not None:
                    print("Error reading from the database:", e)
                equipment_to_update = input(
                    "Please choose an id from the list")
            if any(int(equipment_to_update) in eq for eq in equipment):
                break
            else:
                print("Id does not exist")
        except:
            print("Please enter a valid id.")
    # get new values
    return next(eq for eq in equipment if eq[0] == int(equipment_to_update))


def choose_section(conn):
    """has user choose a section and returns it as a tuple"""
    # choose section to change
    curr = conn.cursor()
    query = "SELECT * FROM section;"
    curr.execute(query)
    section_ids = curr.fetchall()
    while True:
        try:
            section_to_update = input(
                "What is the id of the section you would like to select? Press v to see the sections. ")
            if section_to_update == "v" or section_to_update == "V":
                e = get_all_sections(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            elif any(int(section_to_update) in section for section in section_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    return next(section for section in section_ids if section[0] == int(section_to_update))


def choose_employee(conn):
    """has user choose an employee and returns it as a tuple
    """
    # get new employee
    curr = conn.cursor()
    query = "SELECT * FROM employee;"
    curr.execute(query)
    emp_ids = curr.fetchall()
    while True:
        try:
            employee_id = input(
                "What is the id of the employee? Press v to see the employees. ")
            if employee_id == "v" or employee_id == "V":
                e = get_all_employees(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            elif any(int(employee_id) in emp for emp in emp_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    return next(emp for emp in emp_ids if emp[0] == int(employee_id))


def choose_shift(conn):
    """has user choose a shift and returns it as a tuple
    """
    # choose shift to change
    curr = conn.cursor()
    curr.callproc("view_schedule", ())
    schedule = curr.fetchall()
    while True:
        print("Current Schedule:")
        e = get_schedule(conn)
        if e is not None:
            print("Error reading from the database:", e)
        try:
            shift_to_update = int(
                input("Which shift would you like to select? Please enter the id: "))
            if any(int(shift_to_update) in shift for shift in schedule):
                break
            else:
                print("Id does not exist, please try again.")
        except:
            print("Please enter a valid id.")
    return next(shift for shift in schedule if shift[0] == int(shift_to_update))


def choose_artist(conn):
    """has user choose an artist and returns it as a tuple
    """
    # choose artist to change
    curr = conn.cursor()
    query = "SELECT * FROM artist;"
    curr.execute(query)
    artist_ids = curr.fetchall()
    while True:
        try:
            artist_to_update = input(
                "What is the id of the artist you would like to select? Press v to see the artists. ")
            if artist_to_update == "v" or artist_to_update == "V":
                e = get_all_artists(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            elif any(int(artist_to_update) in artist for artist in artist_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    # get new values
    return next(
        artist for artist in artist_ids if artist[0] == int(artist_to_update))


def choose_customer(conn):
    """has user choose a customer and returns it as a tuple
    """
    # choose customer to change
    curr = conn.cursor()
    query = "SELECT * FROM customer;"
    curr.execute(query)
    customer_ids = curr.fetchall()
    while True:
        try:
            customer_to_update = input(
                "What is the id of the customer? Press v to see the customers. ")
            if customer_to_update == "v" or customer_to_update == "V":
                e = get_all_customers(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            elif any(int(customer_to_update) in customer for customer in customer_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    return next(
        customer for customer in customer_ids if customer[0] == int(customer_to_update))


def choose_genre(conn):
    """has user choose a genre and returns it as a tuple
    """
    # choose genre to change
    curr = conn.cursor()
    query = "SELECT * FROM genre;"
    curr.execute(query)
    genre_ids = curr.fetchall()
    while True:
        try:
            genre_to_update = input(
                "What is the id of the genre? Press v to see the genres. ")
            if genre_to_update == "v" or genre_to_update == "V":
                e = get_all_genres(conn)
                if e is not None:
                    print("Error reading from the database:", e)
            elif any(int(genre_to_update) in genre for genre in genre_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    return next(genre for genre in genre_ids if genre[0] == int(genre_to_update))


def update_employee(conn):
    """updates employee in employee table
    """
    curr = conn.cursor()
    employee_curr = choose_employee(conn)
    name = input(
        "What would you like the new name to be? Enter \"same\" to keep it the same. ")
    if name == "same" or name == "":
        name = employee_curr[1]
    while True:
        salary = input(
            "What would you like the new salary to be? Enter \"same\" to keep it the same. ")
        try:
            if salary == "same" or salary == "":
                salary = employee_curr[2]
            salary = float(salary.replace("$", "").replace(",", ""))
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        is_manager = input("Would you like them to be a manager? (y/n)")
        if is_manager == "y":
            is_manager = True
            break
        elif is_manager == "n":
            is_manager = False
            break
        else:
            print("Not a valid choice. Please enter (y/n)")
    # call procedure
    try:
        curr.callproc("update_employee",
                      (employee_curr[0], name, salary, is_manager))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_shift(conn):
    """updates employee working a shift
    """
    shift_to_update = choose_shift(conn)[0]
    new_employee = choose_employee(conn)[0]
    # call procedure
    try:
        curr = conn.open()
        curr.callproc("change_shift_emp", (shift_to_update, new_employee))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_artist(conn):
    """updates artist in artist table
    """
    artist_curr = choose_artist(conn)
    name = input(
        "What would you like the new name to be? Enter \"same\" to keep it the same. ")
    if name == "same" or name == "":
        name = artist_curr[1]
    lead_singer = input(
        "What would you like the new lead singer to be? Enter \"same\" to keep it the same. ")
    if lead_singer == "same" or lead_singer == "":
        lead_singer = artist_curr[2]
    # call procedure
    try:
        curr = conn.open()
        curr.callproc("update_artist", (artist_curr[0], name, lead_singer))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_customer_by_customer(conn, current_user_id):
    """updates customer with current user id (good for when customer is changing it)
    """
    curr = conn.cursor()
    # get new values
    query = f"SELECT * FROM customer WHERE c_id = {current_user_id};"
    curr.execute(query)
    customer_curr = curr.fetchall()
    customer_curr = customer_curr[0]
    first_name = input(
        "What would you like the new first name to be? Enter \"same\" to keep it the same. ")
    if first_name == "same" or first_name == "":
        first_name = customer_curr[1]
    last_name = input(
        "What would you like the new last name to be? Enter \"same\" to keep it the same. ")
    if last_name == "same" or last_name == "":
        last_name = customer_curr[2]
    email = input(
        "What would you like the new email to be? Enter \"same\" to keep it the same. ")
    if email == "same" or email == "":
        email = customer_curr[3]
    while True:
        cc = input(
            "What would you like the new credit card # to be? Enter \"same\" to keep it the same. ")
        if cc == "same" or cc == "":
            cc = customer_curr[4]
            break
        else:
            try:
                cc = int(cc)
                break
            except:
                print("Please enter a number or \"same\".")
    # call procedure
    try:
        curr.callproc("update_customer", (current_user_id,
                      first_name, last_name, email, cc))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_customer(conn):
    """updates customer (good for when employee is changing it)
    """
    return update_customer(conn, choose_customer(conn)[0])


def update_section(conn):
    """updates section in section table
    """
    # get new values
    section_curr = choose_section(conn)
    title = input(
        "What would you like the new title to be? Enter \"same\" to keep it the same. ")
    if title == "same" or title == "":
        title = section_curr[1]
    description = input(
        "What would you like the new description to be? Enter \"same\" to keep it the same. ")
    if description == "same" or description == "":
        description = section_curr[2]
    # call procedure
    try:
        curr = conn.cursor()
        curr.callproc("update_section", (section_curr[0], title, description))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_record(conn):
    """updates record in records table
    """
    item_curr = choose_record(conn)
    # get new values
    name = input(
        "What would you like the new name to be? Enter \"same\" to keep it the same. ")
    if name == "same" or name == "":
        name = item_curr[4]
    while True:
        price = input(
            "What would you like the new price to be? Enter \"same\" to keep it the same. ")
        try:
            if price == "same" or price == "":
                price = item_curr[1]
            price = float(price.replace("$", "").replace(",", ""))
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        quantity = input(
            "What would you like the new quantity to be? Enter \"same\" to keep it the same. ")
        try:
            if quantity == "same" or quantity == "":
                quantity = item_curr[2]
            quantity = int(quantity)
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        release_year = input(
            "What would you like the new release year to be? Enter \"same\" to keep it the same. ")
        try:
            if release_year == "same" or release_year == "":
                release_year = item_curr[5]
            release_year = int(release_year)
            break
        except:
            print("Please enter a number, or \"same\".")
    # choose genre to change
    curr = conn.cursor()
    query = "SELECT * FROM genre;"
    curr.execute(query)
    genre_ids = curr.fetchall()
    while True:
        try:
            genre_to_update = input(
                "What is the id of the new genre? Enter \"same\" to keep it the same. Press v to see the genres. ")
            if genre_to_update == "v" or genre_to_update == "V":
                for id, name in genre_ids:
                    print("Id:", id, "Name:", name)
            elif genre_to_update == "same" or genre_to_update == "":
                genre_to_update = next(
                    genre_id for genre_id, genre_name in genre_ids if genre_name == item_curr[7])
            elif any(id_to_check == int(genre_to_update) for id_to_check, _ in genre_ids):
                break
            else:
                print("ID does not exist, please try again.")
        except:
            print("Please enter a valid ID.")
    print("You are not allowed to change the artist of the record directly.")
    print("You are not allowed to change the section in the update function. Please use the move feature.")
    # call procedure
    try:
        curr.callproc(
            "update_record", (item_curr[0], price, quantity, name, release_year, genre_to_update))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_record_player(conn):
    """update record player in record_player table
    """
    # get new values
    item_curr = choose_record_player(conn)
    while True:
        disc_size = input(
            "What would you like the new disc size to be? Enter \"same\" to keep it the same. Only 7, 10, and 12 are valid.")
        if disc_size == "same" or disc_size == "":
            disc_size = item_curr[1]
            break
        elif disc_size == '7' or disc_size == '10' or disc_size == '12':
            break
        else:
            print("Not a valid input.")
    while True:
        price = input(
            "What would you like the new price to be? Enter \"same\" to keep it the same. ")
        try:
            if price == "same" or price == "":
                price = item_curr[6]
            price = float(price.replace("$", "").replace(",", ""))
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        quantity = input(
            "What would you like the new quantity to be? Enter \"same\" to keep it the same. ")
        try:
            if quantity == "same" or quantity == "":
                quantity = item_curr[7]
            quantity = int(quantity)
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        year = input(
            "What would you like the new release year to be? Enter \"same\" to keep it the same. ")
        try:
            if year == "same" or year == "":
                year = item_curr[3]
            year = int(year)
            break
        except:
            print("Please enter a number, or \"same\".")
    manufacturer = input(
        "What would you like the new manufacturer to be? Enter \"same\" to keep it the same. ")
    if manufacturer == "same" or manufacturer == "":
        manufacturer = item_curr[2]
    model = input(
        "What would you like the new model to be? Enter \"same\" to keep it the same. ")
    if model == "same" or model == "":
        model = item_curr[4]
    while True:
        bluetooth = input(
            "Would you like it to be bluetooth (y/n)? Enter \"same\" to keep it the same. ")
        if bluetooth == "same" or bluetooth == "":
            bluetooth = item_curr[5]
            break
        elif bluetooth == 'y':
            bluetooth = True
            break
        elif bluetooth == 'n':
            bluetooth = False
            break
        else:
            print("Not a valid input.")
    print("You are not allowed to change the section in the update function. Please use the move feature.")
    # call procedure
    try:
        curr = conn.cursor()
        curr.callproc("update_record_player", (
            item_curr[0], disc_size, manufacturer, year, model, bluetooth, price, quantity))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_equipment(conn):
    """update equipment in equipment table
    """
    item_curr = choose_equipment(conn)
    while True:
        price = input(
            "What would you like the new price to be? Enter \"same\" to keep it the same. ")
        try:
            if price == "same" or price == "":
                price = item_curr[4]
            price = float(price.replace("$", "").replace(",", ""))
            break
        except:
            print("Please enter a number, or \"same\".")
    while True:
        quantity = input(
            "What would you like the new quantity to be? Enter \"same\" to keep it the same. ")
        try:
            if quantity == "same" or quantity == "":
                quantity = item_curr[5]
            quantity = int(quantity)
            break
        except:
            print("Please enter a number, or \"same\".")
    manufacturer = input(
        "What would you like the new manufacturer to be? Enter \"same\" to keep it the same. ")
    if manufacturer == "same" or manufacturer == "":
        manufacturer = item_curr[3]
    name = input(
        "What would you like the new name to be? Enter \"same\" to keep it the same. ")
    if name == "same" or name == "":
        name = item_curr[1]
    description = input(
        "What would you like the new description to be? Enter \"same\" to keep it the same. ")
    if description == "same" or description == "":
        description = item_curr[2]
    print("You are not allowed to change the section in the update function. Please use the move feature.")
    # call procedure
    try:
        curr = conn.cursor()
        curr.callproc("update_equipment",
                      (item_curr[0], name, description, manufacturer, price, quantity))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def move_to_section(conn):
    """updates section_id for a user chosen item
    """
    while True:
        try:
            type = int(
                input("Enter 1 for record, 2 for record player, and 3 for equipment."))
            if type == 1 or type == 2 or type == 3:
                break
            else:
                print("Please enter either 1, 2, or 3.")
        except:
            print("Please enter a valid input (1, 2, 3).")
    if type == 1:
        id_to_update = choose_record(conn)[0]
    elif type == 2:
        id_to_update = choose_record_player(conn)[0]
    elif type == 3:
        id_to_update = choose_equipment(conn)[0]

    section_to_update = choose_section(conn)[0]
    # call procedure
    try:
        curr = conn.cursor()
        curr.callproc("move_section", (id_to_update, section_to_update))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_employee(conn):
    """delete chosen employee
    """
    employee = choose_employee(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_employee", (employee[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_shift(conn):
    """delete chosen shift
    """
    shift = choose_shift(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_shift", (shift[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_artist(conn):
    """delete chosen artist
    """
    artist = choose_artist(conn)
    artist = artist[0]
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_artist", (artist,))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_customer(conn):
    """delete chosen customer
    """
    customer = choose_customer(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_customer", (customer[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_item(conn):
    """delete chosen item
    """
    while True:
        try:
            type = int(
                input("Enter 1 for record, 2 for record player, and 3 for equipment."))
            if type == 1 or type == 2 or type == 3:
                break
        except:
            print("Please enter a valid input.")
    if type == 1:
        id_to_update = choose_record(conn)[0]
    if type == 2:
        id_to_update = choose_record_player(conn)[0]
    if type == 3:
        id_to_update = choose_equipment(conn)[0]
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_item", (id_to_update,))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_genre(conn):
    """delete chosen genre
    """
    genre = choose_genre(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_genre", (genre[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_section(conn):
    """delete chosen section
    """
    section = choose_section(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_section", (section[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_order(conn):
    """delete chosen section
    """
    order = choose_order(conn)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_order", (order[0],))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def delete_order_item(conn):
    """Deletes an item in an order based on selection"""
    order = choose_order(conn)
    item = choose_order_item(conn, order)
    # call delete procedure
    try:
        curr = conn.cursor()
        curr.callproc("delete_order_item", (order[0], item[0]))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def update_employee_overall(conn):
    """Prompts the user to select an entry to update and executes the corresponding function"""
    while True:
        print("Which table would you like to update an entry in?")
        print("1. Artist")
        print("2. Customer")
        print("3. Equipment")
        print("4. Record Player")
        print("5. Record")
        print("6. Section (change description of a section)")
        print("7. Move an item's section (item belongs somewhere else now)")
        print("To change the contents of an order, please delete incorrect items and add correct items.")
        print("If you'd like to change genres, please delete the old one and create a new one.")
        try:
            table_choice = int(input("Enter the corresponding number: "))
            if table_choice == 1:
                update_artist(conn)
                break
            elif table_choice == 2:
                update_customer(conn)
                break
            elif table_choice == 3:
                update_equipment(conn)
                break
            elif table_choice == 4:
                update_record_player(conn)
                break
            elif table_choice == 5:
                update_record(conn)
                break
            elif table_choice == 6:
                update_section(conn)
                break
            elif table_choice == 7:
                move_to_section(conn)
                break
            else:
                print("Please enter a valid number (1-7).")
        except:
            print("Please enter a valid number (1-7).")


def update_manager(conn):
    """Prompts the user to select an entry to update and executes the corresponding function"""
    while True:
        print("Which table would you like to update an entry in?")
        print("1. Artist")
        print("2. Customer")
        print("3. Employee")
        print("4. Equipment")
        print("5. Record Player")
        print("6. Record")
        print("7. Shift")
        print("8. Section (change description of a section)")
        print("9. Move an item's section (item belongs somewhere else now)")
        print("To change the contents of an order, please delete incorrect items and add correct items.")
        print("If you'd like to change genres, please delete the old one and create a new one.")
        print("Managers fall under employee.")
        try:
            table_choice = int(input("Enter the corresponding number: "))
            if table_choice == 1:
                update_artist(conn)
                break
            elif table_choice == 2:
                update_customer(conn)
                break
            elif table_choice == 3:
                update_employee(conn)
                break
            elif table_choice == 4:
                update_equipment(conn)
                break
            elif table_choice == 5:
                update_record_player(conn)
                break
            elif table_choice == 6:
                update_record(conn)
                break
            elif table_choice == 7:
                update_shift(conn)
                break
            elif table_choice == 8:
                update_section(conn)
                break
            elif table_choice == 9:
                move_to_section(conn)
                break
            else:
                print("Please enter a valid number (1-9).")
        except:
            print("Please enter a valid number (1-9).")


def delete_manager(conn):
    """Prompts the user to select an entry to delete and executes the corresponding function"""
    while True:
        print("Which table would you like to delete an entry in?")
        print("1. Artist")
        print("2. Customer")
        print("3. Employee")
        print("4. Item")
        print("5. Order (entire order)")
        print("6. Order item (item in order)")
        print("7. Shift")
        print("8. Section")
        print("9. Genre")
        print("Managers fall under employee.")
        try:
            table_choice = int(input("Enter the corresponding number: "))
            if table_choice == 1:
                delete_artist(conn)
                break
            elif table_choice == 2:
                delete_customer(conn)
                break
            elif table_choice == 3:
                delete_employee(conn)
                break
            elif table_choice == 4:
                delete_item(conn)
                break
            elif table_choice == 5:
                delete_order(conn)
                break
            elif table_choice == 6:
                delete_order_item(conn)
                break
            elif table_choice == 7:
                delete_shift(conn)
                break
            elif table_choice == 8:
                delete_section(conn)
                break
            elif table_choice == 9:
                delete_genre(conn)
                break
            else:
                print("Please enter a valid number (1-9).")
        except Exception as err:
            print(err)
            print("Please enter a valid number (1-9).")


def delete_employee_overall(conn):
    """Prompts the user to select an entry to delete and executes the corresponding function"""
    while True:
        print("Which table would you like to delete an entry in?")
        print("1. Artist")
        print("2. Customer")
        print("3. Order (entire order)")
        print("4. Order item (item in order)")
        print("5. Genre")
        print("Managers fall under employee.")
        try:
            table_choice = int(input("Enter the corresponding number: "))
            if table_choice == 1:
                delete_artist(conn)
                break
            elif table_choice == 2:
                delete_customer(conn)
                break
            elif table_choice == 3:
                delete_order(conn)
                break
            elif table_choice == 4:
                delete_order_item(conn)
                break
            elif table_choice == 5:
                delete_genre(conn)
                break
            else:
                print("Please enter a valid number (1-5).")
        except:
            print("Please enter a valid number (1-5).")
