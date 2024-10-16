import sqlite3
from tkinter import messagebox


db_path = r'C:\Users\user\Documents\LAST\RentalSystemDatabase.db'

def create_connection():
    return sqlite3.connect(db_path)

def initialize_database():
    with create_connection() as conn:
        cursor = conn.cursor()

    # Create Table
    create_table_customer = '''
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName VARCHAR(100) NOT NULL,
        MiddleName VARCHAR(100),
        LastName VARCHAR(100) NOT NULL,
        Address VARCHAR(255) NOT NULL,
        ContactNo INTEGER NOT NULL,
        EmailAddress VARCHAR(100) NOT NULL
    );
    '''

    create_table_event = '''
    CREATE TABLE IF NOT EXISTS Event (
        EventID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INTEGER NOT NULL,
        EventName VARCHAR(100) NOT NULL,
        EventLocation VARCHAR(255) NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    );
    '''

    create_table_rental = '''
    CREATE TABLE IF NOT EXISTS Rental (
        RentalID INTEGER PRIMARY KEY AUTOINCREMENT,
        EventID INTEGER NOT NULL,
        PackageID INTEGER NOT NULL,
        QuantityRented INTEGER NOT NULL,
        RentalDate VARCHAR(10) NOT NULL, 
        ReturnDate VARCHAR(10) NOT NULL, 
        RentalStatus VARCHAR(10) NOT NULL CHECK(RentalStatus IN ('Active', 'Returned')), 
        FOREIGN KEY (EventID) REFERENCES Event(EventID),
        FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
    );

    '''

    create_table_package = '''
    CREATE TABLE IF NOT EXISTS Package (
        PackageID INTEGER PRIMARY KEY AUTOINCREMENT,
        PackageName VARCHAR(100) NOT NULL, 
        QuantityAvailable INTEGER NOT NULL,
        PackagePrice INTEGER NOT NULL
    );
    '''

    create_table_payment = '''
    CREATE TABLE IF NOT EXISTS Payment (
        PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
        RentalID INTEGER NOT NULL,
        PaymentDate VARCHAR(10) NOT NULL, 
        Amount REAL NOT NULL,
        PaymentMethod VARCHAR(10) NOT NULL CHECK(PaymentMethod IN ('Cash', 'E-Wallet')), 
        PaymentStatus VARCHAR(10) NOT NULL CHECK(PaymentStatus IN ('Pending', 'Paid')), 
        FOREIGN KEY (RentalID) REFERENCES Rental(RentalID)
    );
    '''

    create_table_equipment = '''
    CREATE TABLE IF NOT EXISTS Equipment (
        EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        EquipmentName VARCHAR(100) NOT NULL, 
        EquipmentType VARCHAR(50) NOT NULL 
    );
    '''

    create_table_equipmentpackages = '''
    CREATE TABLE IF NOT EXISTS EquipmentPackage (
        PackageID INTEGER NOT NULL, 
        EquipmentID INTEGER NOT NULL, 
        EquipmentUnit INTEGER NOT NULL, 
        PRIMARY KEY (EquipmentID, PackageID),
        FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
        FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
    );
    '''

    # Execute queries to create tables
    cursor.execute(create_table_customer)
    cursor.execute(create_table_event)
    cursor.execute(create_table_package)
    cursor.execute(create_table_rental)
    cursor.execute(create_table_payment)
    cursor.execute(create_table_equipment)
    cursor.execute(create_table_equipmentpackages)

    # Commit changes
    conn.commit()

    # For debugging
    print("Tables created successfully")

db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'

def insert_customer_to_db(first_name, middle_name, last_name, phone, address, email):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            insert_query = '''
            INSERT INTO Customer (FirstName, MiddleName, LastName, ContactNo, Address, EmailAddress)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_query, (first_name, middle_name, last_name, phone, address, email))

            # Retrieve the last inserted customer row id
            customer_id = cursor.lastrowid

            return customer_id

    except sqlite3.Error as e:
        print(f"Error inserting customer data: {e}")
        return None

def insert_event_to_db(customer_id, event_name, event_location):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            insert_query = '''
            INSERT INTO Event (CustomerID, EventName, EventLocation)
            VALUES (?, ?, ?)
            '''
            cursor.execute(insert_query, (customer_id, event_name, event_location))

            # Retrieve the last inserted event row id
            event_id = cursor.lastrowid

            return event_id

    except sqlite3.Error as e:
        print(f"Error inserting event data: {e}")
        return None

def insert_rental_to_db(event_id, package_id, quantity_rented, rental_date, return_date, rental_status):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            insert_query = '''
            INSERT INTO Rental (EventID, PackageID, QuantityRented, RentalDate, ReturnDate, RentalStatus)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_query, (event_id, package_id, quantity_rented, rental_date, return_date, rental_status))

            # Retrieve the last inserted rental row id
            rental_id = cursor.lastrowid

            return rental_id

    except sqlite3.Error as e:
        print(f"Error inserting rental data: {e}")
        return None

def insert_payment_to_db(rental_id, payment_date, amount, payment_method, payment_status):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            insert_query = '''
            INSERT INTO Payment (RentalID, PaymentDate, Amount, PaymentMethod, PaymentStatus)
            VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_query, (rental_id, payment_date, amount, payment_method, payment_status))

            # Retrieve the last inserted payment row id
            payment_id = cursor.lastrowid

            return payment_id

    except sqlite3.Error as e:
        print(f"Error inserting payment data: {e}")
        return None

# Function to query total rentals
def fetch_total_rentals():
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Query to count total rentals
        cursor.execute("SELECT COUNT(*) FROM Rental")
        total_rentals = cursor.fetchone()[0]  # Fetch the count value

        conn.commit()
        conn.close()

        return total_rentals

    except sqlite3.Error as e:
        print(f"Error fetching total rentals: {e}")
        return None

# Function to fetch data from the database
def fetch_returned_rentals():
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        query = """
        SELECT 
            Rental.RentalID, 
            Customer.CustomerID, 
            Event.EventID, 
            Payment.PaymentID,
            Customer.FirstName || ' ' || Customer.LastName AS CustomerName,
            Rental.RentalDate, 
            Rental.ReturnDate, 
            Rental.RentalStatus
        FROM 
            Rental
        JOIN 
            Event ON Rental.EventID = Event.EventID
        JOIN 
            Customer ON Event.CustomerID = Customer.CustomerID
        JOIN 
            Payment ON Rental.RentalID = Payment.RentalID
        WHERE 
            Rental.RentalStatus = 'Returned';
        """

        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()

        conn.commit()
        conn.close()

        return results

    except sqlite3.Error as e:
        print(f"Error fetching returned rentals: {e}")
        return []


# Function to fetch total pending payments
def fetch_total_pending_payments():
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) AS TotalPendingCount
            FROM Payment
            WHERE PaymentStatus = 'Pending';
        ''')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except sqlite3.Error as e:
        print(f"Error fetching total pending payments: {e}")
        return None


def soft_delete_rental(rental_id):
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Update RentalStatus to 'Deleted'
        cursor.execute("UPDATE Rental SET RentalStatus = 'Deleted' WHERE RentalID = ?", (rental_id,))
        conn.commit()
        conn.close()

        print(f"Rental ID {rental_id} marked as Deleted.")

    except sqlite3.Error as e:
        print(f"Error performing soft delete: {e}")


#to update status
def return_rental(rental_id, package_id):
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Update PaymentStatus to 'Paid'
        cursor.execute("UPDATE Payment SET PaymentStatus = 'Paid' WHERE RentalID = ?", (rental_id,))

        # Update RentalStatus to 'Returned'
        cursor.execute("UPDATE Rental SET RentalStatus = 'Returned' WHERE RentalID = ?", (rental_id,))

        # Increment QuantityAvailable in Package table
        cursor.execute("UPDATE Package SET QuantityAvailable = QuantityAvailable + 1 WHERE PackageID = ?", (package_id,))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error updating rental: {e}")

# Function to fetch monthly earnings data
def fetch_monthly_earnings():
    try:
        db_file = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%m', PaymentDate) AS Month, SUM(Amount) AS TotalEarnings
            FROM Payment
            WHERE PaymentStatus = 'Paid'
            GROUP BY Month
            ORDER BY Month;
        ''')
        results = cursor.fetchall()
        conn.close()

        # Process results to return data in list form
        monthly_earnings = [0] * 12  # Initialize a list with 12 zeros for each month
        for result in results:
            month_index = int(result[0]) - 1  # Convert month string to zero-based index
            monthly_earnings[month_index] = result[1]

        return monthly_earnings
    except sqlite3.Error as e:
        print(f"Error fetching monthly earnings: {e}")
        return []


def fetch_rental_details(rental_id, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Rental WHERE RentalID = ?", (rental_id,))
        rental_data = cursor.fetchone()
        return rental_data
    except sqlite3.Error as e:
        print("Error fetching rental data:", e)
        return None
    finally:
        conn.close()


def fetch_customer_details(customer_id, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Customer WHERE CustomerID = ?", (customer_id,))
        customer_data = cursor.fetchone()
        return customer_data
    except sqlite3.Error as e:
        print("Error fetching customer data:", e)
        return None
    finally:
        conn.close()

# Function to fetch all packages from the database
def fetch_all_packages():
    with create_connection() as conn:
        cursor = conn.cursor()

        select_query = '''
        SELECT PackageID, PackageName, QuantityAvailable, PackagePrice FROM Package
        '''

        cursor.execute(select_query)
        packages = cursor.fetchall()

        return packages


# Function to fetch package price from the database
def fetch_package_price(package_id):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        select_query = '''
        SELECT PackagePrice FROM Package WHERE PackageID = ?
        '''
        cursor.execute(select_query, (package_id,))
        row = cursor.fetchone()

        if row:
            package_price = row[0]
            return package_price
        else:
            raise ValueError(f"Package with ID {package_id} not found")

    except sqlite3.Error as e:
        print(f"Error fetching package price: {e}")
        raise
    finally:
        conn.close()

def fetch_customer_data():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            c.CustomerID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            c.Address,
            c.ContactNo,
            c.EmailAddress,
            e.EventName,
            e.EventLocation
        FROM
            Customer c
        LEFT JOIN Event e ON c.CustomerID = e.CustomerID;
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching customer data: {e}")
        return []

def fetch_customer_by_id(customer_id):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            CustomerID,
            FirstName,
            MiddleName,
            LastName,
            Address,
            ContactNo,
            EmailAddress
        FROM
            Customer
        WHERE
            CustomerID = ?;
        '''

        cursor.execute(query, (customer_id,))
        customer_data = cursor.fetchone()

        conn.close()

        return customer_data

    except sqlite3.Error as e:
        print(f"Error fetching customer data by ID: {e}")
        return []



def update_customer_in_db(customer_id, first_name, middle_name, last_name, address, contact_no, email):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        UPDATE Customer
        SET
            FirstName = ?,
            MiddleName = ?,
            LastName = ?,
            Address = ?,
            ContactNo = ?,
            EmailAddress = ?
        WHERE
            CustomerID = ?;
        '''

        cursor.execute(query, (first_name, middle_name, last_name, address, contact_no, email, customer_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Customer details updated successfully")

    except sqlite3.Error as e:
        print(f"Error updating customer data: {e}")
        messagebox.showerror("Error", "Failed to update customer details")



def fetch_rental_data():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            r.RentalID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            pa.Amount AS TotalAmount,
            p.PackageName,
            r.RentalDate AS RentalStart,
            r.ReturnDate,
            pa.PaymentStatus,
            r.RentalStatus
        FROM
            Rental r
        JOIN Event e ON r.EventID = e.EventID
        JOIN Customer c ON e.CustomerID = c.CustomerID
        JOIN Package p ON r.PackageID = p.PackageID
        JOIN Payment pa ON r.RentalID = pa.RentalID
        WHERE
            r.RentalStatus <> 'Deleted';
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching rental data: {e}")
        return []


def fetch_payment_data():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            r.RentalID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            pa.Amount AS TotalAmount,
            p.PackageName,
            r.RentalDate AS RentalStart,
            r.ReturnDate,
            pa.PaymentStatus,
            pa.PaymentMethod
        FROM
            Rental r
        JOIN Event e ON r.EventID = e.EventID
        JOIN Customer c ON e.CustomerID = c.CustomerID
        JOIN Package p ON r.PackageID = p.PackageID
        JOIN Payment pa ON r.RentalID = pa.RentalID;
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching rental data: {e}")
        return []


def fetch_available_packages():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            PackageID,
            PackageName,
            PackagePrice AS RentalPrice,
            QuantityAvailable AS Quantity
        FROM
            Package;
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching available packages: {e}")
        return []


def fetch_rented_packages():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
        SELECT
            p.PackageID,
            p.PackageName,
            p.PackagePrice AS RentalPrice,
            SUM(r.QuantityRented) AS TotalRented
        FROM
            Package p
        LEFT JOIN
            Rental r ON p.PackageID = r.PackageID
        GROUP BY
            p.PackageID, p.PackageName, p.PackagePrice, p.QuantityAvailable;
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching rented packages: {e}")
        return []


def fetch_event_by_customer_id(customer_id):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Event WHERE CustomerID = ?", (customer_id,))
        event_data = cursor.fetchall()  # Fetch all events for the customer
        return event_data
    except sqlite3.Error as e:
        print(f"Error fetching event data: {e}")
        return None


def update_event_in_db(event_id, customer_id, event_name, event_location):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE Event SET EventName = ?, EventLocation = ? WHERE EventID = ? AND CustomerID = ?",
                       (event_name, event_location, event_id, customer_id))
        conn.commit()
        print("Event updated successfully")
    except sqlite3.Error as e:
        print(f"Error updating event: {e}")
        conn.rollback()


def fetch_total_customers():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get total number of customers
        cursor.execute("SELECT COUNT(*) FROM Customer;")
        total_customers = cursor.fetchone()[0]

        conn.close()

        return total_customers

    except sqlite3.Error as e:
        print(f"Error fetching total customers: {e}")
        return -1  # Return an error value or handle as needed


def delete_rental(rental_id):
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Delete the rental from the database
        cursor.execute("DELETE FROM Rental WHERE RentalID = ?", (rental_id,))
        conn.commit()

        conn.close()
        return True  # Return True if deletion is successful

    except sqlite3.Error as e:
        print(f"Error deleting rental: {e}")
        return False  # Return False if deletion fails


def fetch_package_equipment():
    try:
        db_path = r'C:\Users\Lenovo\PycharmProjects\pythonProject2\RentalSystemDatabase.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
 SELECT
    p.PackageID,
    p.PackageName,
    GROUP_CONCAT(e.EquipmentName, ', ') AS IncludedEquipment
FROM
    Package p
JOIN
    EquipmentPackage ep ON p.PackageID = ep.PackageID
JOIN
    Equipment e ON ep.EquipmentID = e.EquipmentID
GROUP BY
    p.PackageID, p.PackageName;

        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    except sqlite3.Error as e:
        print(f"Error fetching package equipment: {e}")
        return []



def decrease_package_quantity(package_id):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            sql_update_quantity = """
                UPDATE Package
                SET QuantityAvailable = QuantityAvailable - 1
                WHERE PackageID = ?
            """
            cursor.execute(sql_update_quantity, (package_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Error updating package quantity: {e}")
        return False




def fetch_rental_details_to_update(rental_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Fetch customer data
            cursor.execute(
                "SELECT * FROM Customer WHERE CustomerID = (SELECT CustomerID FROM Rental WHERE RentalID = ?)",
                (rental_id,))
            customer_data = cursor.fetchone()

            # Fetch event data
            cursor.execute("SELECT * FROM Event WHERE EventID = (SELECT EventID FROM Rental WHERE RentalID = ?)",
                           (rental_id,))
            event_data = cursor.fetchone()

            # Fetch rental data
            cursor.execute("SELECT * FROM Rental WHERE RentalID = ?", (rental_id,))
            rental_data = cursor.fetchone()

            # Fetch payment data
            cursor.execute("SELECT * FROM Payment WHERE RentalID = ?", (rental_id,))
            payment_data = cursor.fetchone()

            return {
                "customer": customer_data,
                "event": event_data,
                "rental": rental_data,
                "payment": payment_data
            }

    except sqlite3.Error as e:
        print(f"Error fetching rental details: {e}")
        return None

