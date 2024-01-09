import pymysql


def get_number_input(prompt):
    """makes them give a number for input"""
    while True:
        try:
            number = int(input(prompt))
            break
        except:
            print("Please enter a number.")
    return number


def get_money_input(prompt):
    """makes them give a number for input"""
    while True:
        try:
            number = float(input(prompt).replace("$", "").replace(",", ""))
            break
        except:
            print("Please enter a number.")
    return number

# Create functions


def add_artist(conn):
    """Inserts a new artist into the artist table"""
    name = input("Enter the artist name: ")
    lead_singer = input("Enter the lead singer: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_artist", (name, lead_singer))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_genre(conn):
    """Inserts a new genre into the genre table"""
    genre_name = input("Enter the genre name: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_genre", (genre_name,))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_customer(conn):
    """Inserts a new customer into the customer table"""
    first_name = input("Enter the customer's first name: ")
    last_name = input("Enter the customer's last name: ")
    email = input("Enter the customer's email: ")
    credit_card_number = get_number_input(
        "Enter the customer's credit card number: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_customer", (first_name,
                      last_name, email, credit_card_number))
        c_id = curr.fetchall()
        conn.commit()
        return c_id
    except pymysql.Error as err:
        return err


def add_employee(conn):
    """Inserts a new employee into the employee table"""
    name = input("Enter the employee name: ")
    salary = get_money_input("Enter the employee salary: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_employee", (name, salary))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_manager(conn):
    """Inserts a new manager into the employee table"""
    name = input("Enter the manager name: ")
    salary = get_money_input("Enter the manager salary: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_manager", (name, salary))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_equipment(conn):
    """Inserts a new piece of equipment into the equipment table"""
    name = input("Enter the equipment name: ")
    description = input("Enter the equipment description: ")
    manufacturer = input("Enter the equipment manufacturer: ")
    price = get_money_input("Enter the equipment price: ")
    quantity = get_number_input("Enter the equipment quantity: ")
    section_id = get_number_input("Enter the section ID: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_equipment", (name, description,
                      manufacturer, price, quantity, section_id))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_record_player(conn):
    """Inserts a new record player into the record_player table"""
    while True:
        disc_size = str(
            input("Enter the record player disc size (7, 10, 12): "))
        if disc_size == '7' or disc_size == '10' or disc_size == '12':
            break
        else:
            print("Please enter 7, 10, or 12.")
    manufacturer = input("Enter the record player manufacturer: ")
    year = get_number_input("Enter the record player year: ")
    model = input("Enter the record player model: ")
    bluetooth = input("Does the record player have Bluetooth?: ")
    price = get_money_input("Enter the record player price: ")
    quantity = get_number_input("Enter the record player quantity: ")
    section = get_number_input("Enter the record player section: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_record_player", (disc_size, manufacturer,
                      year, model, bluetooth, price, quantity, section))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_record(conn):
    """Inserts a new record into the records table"""
    name = input("Enter the record name: ")
    year = get_number_input("Enter the record year: ")
    artist_id = get_number_input("Enter the artist ID: ")
    genre_id = get_number_input("Enter the genre ID: ")
    price = get_money_input("Enter the record price: ")
    quantity = get_number_input("Enter the record quantity: ")
    section_id = get_number_input("Enter the section ID: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_record", (name, year, artist_id,
                      genre_id, price, quantity, section_id))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_order_item(conn):
    """Inserts a new item to the order_items table"""
    order_id = get_number_input("Enter the order ID: ")
    item_id = get_number_input("Enter the item ID: ")
    quantity = get_number_input("Enter the quantity: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_order_item", (order_id, item_id, quantity))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_shift(conn):
    """Inserts a new shift in the shifts table"""
    day_of_week = input("Enter the day of the week: ")
    start_hr = input("Enter the start hour: ")
    end_hr = input("Enter the end hour: ")
    employee_id = get_number_input("Enter the employee ID: ")
    try:
        curr = conn.cursor()
        curr.callproc("add_shift", (day_of_week,
                      start_hr, end_hr, employee_id))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


def add_order(conn, customer_id, location):
    """inserts a new order into the database"""
    try:
        curr = conn.cursor()
        curr.callproc("create_order", (customer_id, location))
        conn.commit()
        return 1
    except pymysql.Error as err:
        return err


# Read functions


def get_all_records(conn):
    """returns all the records from the records table"""
    try:
        cursor = conn.cursor()
        cursor.callproc('view_all_records', ())
        records = cursor.fetchall()
        if records:
            print("Here are all the records in the database:")
            for record in records:
                print(record)
        else:
            print("Error retrieving records: ", records)
    except pymysql.Error as err:
        return err


def get_all_record_players(conn):
    """returns all the record players from the record_player table"""
    try:
        cursor = conn.cursor()
        cursor.callproc('view_all_recordplayers', ())
        record_players = cursor.fetchall()
        if record_players:
            print("Here are all the record players in the database:")
            for player in record_players:
                print(player)
        else:
            print("Error retrieving record players: ", record_players)
    except pymysql.Error as err:
        return err


def get_all_equipment(conn):
    """returns all the equipment from the equipment table"""
    try:
        cursor = conn.cursor()
        cursor.callproc('view_all_equipment', ())
        equipment = cursor.fetchall()
        if equipment:
            print("Here are all the equipment in the database:")
            for item in equipment:
                print(item)
        else:
            print("Error retrieving equipment: ", equipment)
    except pymysql.Error as err:
        return err


def get_schedule(conn):
    """ returns all the schedules from the schedule table"""
    try:
        cursor = conn.cursor()
        cursor.callproc('view_schedule', ())
        schedule = cursor.fetchall()
        if schedule:
            print("Here is the schedule in the database:")
            for shift in schedule:
                print(shift)
        else:
            print("Error retrieving schedule: ", schedule)
    except pymysql.Error as err:
        return err


def get_all_employees(conn):
    """ returns all the employees from the employee table"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employee;')
        employees = cursor.fetchall()
        if employees:
            print("Here are the emnployees in the database:")
            for emp in employees:
                print(emp)
        else:
            print("Error retrieving employees: ", employees)
    except pymysql.Error as err:
        return err


def get_all_sections(conn):
    """ returns all the sections from the section table"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM section;')
        sections = cursor.fetchall()
        if sections:
            print("Here are the sections in the database:")
            for section in sections:
                print(section)
        else:
            print("Error retrieving sections: ", sections)
    except pymysql.Error as err:
        return err


def get_all_artists(conn):
    """ returns all the artists from the artist table"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artist;')
        artists = cursor.fetchall()
        if artists:
            print("Here are the artists in the database:")
            for artist in artists:
                print(artist)
        else:
            print("Error retrieving artists: ", artists)
    except pymysql.Error as err:
        return err


def get_all_genres(conn):
    """ returns all the genres from the genre table"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM genre;')
        genres = cursor.fetchall()
        if genres:
            print("Here are the genres in the database:")
            for genre in genres:
                print(genre)
        else:
            print("Error retrieving genres: ", genres)
    except pymysql.Error as err:
        return err


def get_all_customers(conn):
    """ returns all the customers from the customer table"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customer;')
        customers = cursor.fetchall()
        if customers:
            print("Here are the customers in the database:")
            for customer in customers:
                print(customer)
        else:
            print("Error retrieving customers: ", customer)
    except pymysql.Error as err:
        return err


def get_orders(conn):
    """ returns all the orders from the order table"""
    try:
        curr = conn.cursor()
        curr.callproc("view_all_orders", ())
        orders = curr.fetchall()
        grouped_orders = {}
        for order in orders:
            order_id, item_id, quantity = order
            if order_id not in grouped_orders:
                grouped_orders[order_id] = []
            grouped_orders[order_id].append((item_id, quantity))

        # Print the grouped orders
        for order_id, items in grouped_orders.items():
            print(f"Order ID: {order_id}")
            for item in items:
                item_id, quantity = item
        print(f"  Item ID: {item_id}, Quantity: {quantity}")
    except pymysql.Error as err:
        return err


def get_customer_orders(conn, customer_id):
    """ returns the orders from the order table for the given customer"""
    try:
        curr = conn.cursor()
        curr.callproc("view_customer_details", (customer_id,))
        orders = curr.fetchall()
        orders_grouped = {}
        # Group the items based on the order
        # order id, item id, quantity, i.price, r.name
        for item in orders:
            order = item[0]
            if order in orders:
                orders_grouped[order].extend(
                    e for e in item[1:] if e is not None)
            else:
                orders_grouped[order] = [e for e in item[1:] if e is not None]
        for order, items in orders_grouped.items():
            print("Order Id:", order)
            for item in items:
                print("Item id:", items[0], "Name:", items[4],
                      "Price:", items[3], "Quantity:", items[2])
            print()
    except pymysql.Error as err:
        return err
# Read function for managers
