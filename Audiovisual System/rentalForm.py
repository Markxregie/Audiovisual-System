import customtkinter as ctk
from customtkinter import *
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry
from database_connection import fetch_all_packages, insert_rental_to_db, insert_event_to_db, insert_customer_to_db,insert_payment_to_db, fetch_package_price
from tkinter import messagebox
from enums import RentalStatus, PaymentStatus
from database_connection import fetch_rental_data, fetch_customer_data, decrease_package_quantity, return_rental, update_customer_in_db, fetch_customer_by_id, fetch_payment_data
import re

class Rental(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.main_frame = ctk.CTkFrame(self.master)

        # Create the main frame
        schedule_fm = ctk.CTkFrame(self.master, fg_color='#fefded', height=800)
        schedule_fm.pack(fill='both', expand=True)

        # To fill the main frame
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Date and Time update function
        def updateTime():
            now = datetime.now()
            formatted_time = now.strftime("%A: %B %d, %Y, %I:%M%p")
            DateTime.configure(text=formatted_time)
            schedule_fm.after(1000, updateTime)

        # Title
        rentals = ctk.CTkLabel(schedule_fm, text="Rentals", font=('Century Gothic', 42, 'bold'),
                                   text_color='#154734')
        rentals.grid(row=1, column=0, padx=65, pady=20, sticky='w')

        DateTime = ctk.CTkLabel(schedule_fm, text="", font=('Century Gothic', 20), text_color='#154734')
        DateTime.grid(row=1, column=0, padx=1100, pady=20, sticky='wn')
        updateTime()

        # Search Function
        def search():
            search_term = SearchEntry.get().lower()
            # Searching in Rental Tab
            for item in datagridview.get_children():
                values = datagridview.item(item, "values")
                if any(search_term in str(value).lower() for value in values):
                    datagridview.selection_set(item)
                    datagridview.see(item)
                    datagridview.item(item, tags=())  # Clear any tags to reset appearance
                else:
                    datagridview.selection_remove(item)
                    datagridview.detach(item)  # Hide rows that do not match

            # Searching in Customer Tab
            for item in datagridview1.get_children():
                values = datagridview1.item(item, "values")
                if any(search_term in str(value).lower() for value in values):
                    datagridview1.selection_set(item)
                    datagridview1.see(item)
                    datagridview1.item(item, tags=())  # Clear any tags to reset appearance
                else:
                    datagridview1.selection_remove(item)
                    datagridview1.detach(item)  # Hide rows that do not match

        # Search Rentals
        SearchLabel = ctk.CTkLabel(schedule_fm, text="Search:", text_color='#154734',
                                   font=('Century Gothic', 20, 'bold'))
        SearchLabel.grid(row=2, column=0, padx=400, pady=0, sticky='w')
        SearchEntry = ctk.CTkEntry(schedule_fm, width=370, font=('Century Gothic', 20),
                                   placeholder_text="Search Rentals...")
        SearchEntry.grid(row=2, column=0, padx=490, pady=10, sticky='w')
        SearchButton = ctk.CTkButton(schedule_fm, text="Search", font=('Century Gothic', 20, 'bold'),
                                     fg_color='#154734', text_color='white', hover_color='gray', command=search)
        SearchButton.grid(row=2, column=0, padx=870, pady=10, sticky='w')


        def create_rental_window():
            create_window = CTkToplevel()
            create_window.title("RENTAL FORM")
            create_window.geometry("1100x700")
            create_window.configure(fg_color='#fefded')
            set_appearance_mode('light')
            create_window.grab_set()
            create_window.resizable(False, False)

            def BackRental():
                create_window.destroy()
                self.master.deiconify()
                self.master.lift()

            # Function to validate phone number
            def validate_phone():
                phone_number = PhoneEntry.get()
                if not phone_number.isdigit():
                    messagebox.showerror("Invalid Input", "Phone number must contain only digits.")
                    return False
                return True

            # Function to validate email address
            def validate_email():
                email = EmailEntry.get()
                if not email.endswith("@gmail.com"):
                    messagebox.showerror("Invalid Input", "Email must end with @gmail.com.")
                    return False
                return True

            # MAIN FRAME
            frame1 = CTkScrollableFrame(create_window, fg_color='#f1f1f1', width=950, height=950)
            frame1.grid(row=1, column=0, padx=25, pady=25, sticky='nsew')

            create_window.grid_rowconfigure(1, weight=1)
            create_window.grid_columnconfigure(0, weight=1)

            # TITLE
            RentalForm = CTkLabel(frame1, text="Rental Form", text_color='#154734', font=('Century Gothic', 28, 'bold'))
            RentalForm.grid(row=0, column=0, padx=25, pady=10, sticky='w')

            # Customer Name
            CustLName = CTkLabel(frame1, text="CUSTOMER NAME:", text_color='black', font=('Century Gothic', 18))
            CustLName.grid(row=1, column=0, padx=25, pady=10, sticky='w')
            # LNAME
            CustLNameEntry = CTkEntry(frame1, width=260, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                      corner_radius=10,
                                      font=('Century Gothic', 18), placeholder_text="Last Name")
            CustLNameEntry.grid(row=1, column=0, padx=200, pady=10, sticky='w')
            # FNAME
            CustFNameEntry = CTkEntry(frame1, width=260, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                      corner_radius=10,
                                      font=('Century Gothic', 18), placeholder_text="First Name")
            CustFNameEntry.grid(row=1, column=0, padx=470, pady=10, sticky='w')
            # MNAME
            CustMNameEntry = CTkEntry(frame1, width=260, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                      corner_radius=10,
                                      font=('Century Gothic', 18), placeholder_text="Middle Name")
            CustMNameEntry.grid(row=1, column=0, padx=740, pady=10, sticky='w')

            # ADDRESS
            AddressEntry = CTkLabel(frame1, text="ADDRESS:", text_color='black', font=('Century Gothic', 18))
            AddressEntry.grid(row=2, column=0, padx=25, pady=10, sticky='w')
            AddressEntryField = CTkEntry(frame1, width=350, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                         corner_radius=10,
                                         font=('Century Gothic', 18),
                                         placeholder_text="House No., Street, Barangay, City")
            AddressEntryField.grid(row=2, column=0, padx=125, pady=10, sticky='w')

            # PHONE
            Phone = CTkLabel(frame1, text="PHONE:", text_color='black', font=('Century Gothic', 18))
            Phone.grid(row=3, column=0, padx=25, pady=10, sticky='w')
            PhoneEntry = CTkEntry(frame1, width=350, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                  corner_radius=10,
                                  font=('Century Gothic', 18), placeholder_text="09XX-XXX-XXXX")
            PhoneEntry.grid(row=3, column=0, padx=125, pady=10, sticky='w')

            # EMAIL
            Email = CTkLabel(frame1, text="EMAIL:", text_color='black', font=('Century Gothic', 18))
            Email.grid(row=4, column=0, padx=25, pady=10, sticky='w')
            EmailEntry = CTkEntry(frame1, width=350, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                  corner_radius=10,
                                  font=('Century Gothic', 18),
                                  placeholder_text="example@gmail.com")
            EmailEntry.grid(row=4, column=0, padx=125, pady=10, sticky='w')

            # EVENT
            EventNameLabel = CTkLabel(frame1, text="EVENT:", text_color='black', font=('Century Gothic', 18))
            EventNameLabel.grid(row=2, column=0, padx=520, pady=10, sticky='w')
            EventNameEntry = CTkEntry(frame1, width=405, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                      corner_radius=10,
                                      font=('Century Gothic', 18), placeholder_text="Event Name...")
            EventNameEntry.grid(row=2, column=0, padx=595, pady=10, sticky='w')

            # EVENT LOCATION
            EventLocLabel = CTkLabel(frame1, text="EVENT LOCATION:", text_color='black', font=('Century Gothic', 18))
            EventLocLabel.grid(row=3, column=0, padx=520, pady=10, sticky='w')
            EventLocEntry = CTkEntry(frame1, width=310, height=35, fg_color="#D9D9D9", border_color="#D9D9D9",
                                     corner_radius=10,
                                     font=('Century Gothic', 18), placeholder_text="Event Location...")
            EventLocEntry.grid(row=3, column=0, padx=690, pady=10, sticky='w')

            # RETURN DATE
            ReturnDate = CTkLabel(frame1, text="RETURN DATE:", text_color='black', font=('Century Gothic', 18))
            ReturnDate.grid(row=4, column=0, padx=520, pady=10, sticky='w')
            ReturnDateEntry = DateEntry(frame1, width=10, font=('Century Gothic', 14), date_pattern='yyyy-mm-dd')
            ReturnDateEntry.grid(row=4, column=0, padx=660, pady=10, sticky='w')
            separator = ttk.Separator(frame1, orient='horizontal')
            separator.grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')

            # PACKAGE LABEL
            PackageLabel = CTkLabel(frame1, text="PACKAGE", text_color='#154734', font=('Century Gothic', 20, 'bold'))
            PackageLabel.grid(row=8, column=0, padx=50, pady=10, sticky='w')


            # Fetch packages from the database
            packages = fetch_all_packages()

            # Create radio buttons and price labels for packages
            package_selection = IntVar()
            package_selection.set(-1)  # no selection

            row_num = 9  # Adjust row_num to match the label row
            for package in packages:
                package_id, package_name, quantity_available, price = package

                # Radio button for the package with price text and quantity available
                package_button = CTkRadioButton(frame1,
                                                text=f"{package_name}    Price: P{price}   Available: {quantity_available}",
                                                variable=package_selection,
                                                value=package_id, font=('Century Gothic', 18))
                package_button.grid(row=row_num, column=0, padx=(50, 50), pady=(5, 10), sticky='w')

                row_num += 1


            separator = ttk.Separator(frame1, orient='horizontal')
            separator.grid(row=14, column=0, columnspan=2, pady=10, sticky='ew')

            PaymentMethod = CTkLabel(frame1, text="PAYMENT METHOD", text_color='#154734', font=('Century Gothic', 20, 'bold'))
            PaymentMethod.grid(row=15, column=0, padx=50, pady=10, sticky='w')

            PaymentMethod = CTkComboBox(frame1, values=["Cash", "E-Wallet"], font=('Century Gothic', 18), width=180)
            PaymentMethod.grid(row=16, column=0, padx=50, pady=10, sticky='w')

            def clear_fields():
                CustFNameEntry.delete(0, 'end')
                CustMNameEntry.delete(0, 'end')
                CustLNameEntry.delete(0, 'end')
                PhoneEntry.delete(0, 'end')
                AddressEntryField.delete(0, 'end')
                EmailEntry.delete(0, 'end')
                EventNameEntry.delete(0, 'end')
                EventLocEntry.delete(0, 'end')
                ReturnDateEntry.set_date(None)  # Adjust this line based on your date picker widget
                package_selection.set(-1)
                PaymentMethod.set('')

            def validate_phone(phone_number):
                # Check if the phone number consists only of digits
                if phone_number.isdigit():
                    return True
                else:
                    messagebox.showwarning("Error", "Phone number should only contain digits.")
                    return False

            def validate_email(email):
                # Check if the email ends with "@gmail.com"
                if email.endswith("@gmail.com"):
                    return True
                else:
                    messagebox.showwarning("Error", "Please enter a valid Gmail address.")
                    return False

            def calculate_rent_duration(rental_date, return_date):
                # Calculate rental duration in days
                delta = return_date - rental_date
                return delta.days  # Returns the number of days between rental_date and return_date

            def submit_form():
                # Retrieve form data
                first_name = CustFNameEntry.get().strip()
                middle_name = CustMNameEntry.get().strip()
                last_name = CustLNameEntry.get().strip()
                phone = PhoneEntry.get().strip()
                address = AddressEntryField.get().strip()
                email = EmailEntry.get().strip()
                event_name = EventNameEntry.get().strip()
                event_location = EventLocEntry.get().strip()

                # Validate required fields
                if not (first_name and last_name and phone and address and email and event_name and event_location):
                    messagebox.showwarning("Error", "Please fill in all required fields.")
                    return

                # Allow middle name to be None if not provided
                if middle_name == "":
                    middle_name = None

                # Validate phone number and email
                if not validate_phone(phone):
                    return

                if not validate_email(email):
                    return

                # Retrieve package ID and validate that a package is selected
                selected_package_id = package_selection.get()
                if selected_package_id <= 0:
                    messagebox.showerror("Error", "Please select a valid package.")
                    return

                # Retrieve payment method
                payment_method = PaymentMethod.get()

                # Ensure payment method is selected
                if not payment_method:
                    messagebox.showwarning("Error", "Please select a payment method.")
                    return

                try:
                    # Automatically set rental date to current date and time
                    rental_date = datetime.now().date()

                    # Validate and convert return date
                    try:
                        return_date = ReturnDateEntry.get_date()
                        if not return_date:
                            messagebox.showwarning("Error", "Please select a return date.")
                            return

                        # Ensure return date is after rental date
                        if return_date <= rental_date:
                            messagebox.showwarning("Error", "Return date must be after the rental date.")
                            return
                    except Exception as e:
                        messagebox.showwarning("Error", f"Invalid return date selection: {str(e)}")
                        return

                    # Calculate rental duration in days
                    rental_duration = calculate_rent_duration(rental_date, return_date)

                    # Insert customer data into the database
                    customer_id = insert_customer_to_db(first_name, middle_name, last_name, phone, address, email)
                    if customer_id is None:
                        messagebox.showerror("Error", "Failed to insert customer data.")
                        return
                    print(f"Inserted customer ID: {customer_id}")  # For debugging

                    # Insert event data into the database
                    event_id = insert_event_to_db(customer_id, event_name, event_location)
                    if event_id is None:
                        messagebox.showerror("Error", "Failed to insert event data.")
                        return
                    print(f"Inserted event ID: {event_id}")  # For debugging

                    # Insert rental data
                    quantity_rented = 1
                    rental_status = RentalStatus.ACTIVE
                    rental_id = insert_rental_to_db(event_id, selected_package_id, quantity_rented,
                                                    rental_date.isoformat(), return_date.isoformat(),
                                                    rental_status.value)

                    if rental_id is None:
                        messagebox.showerror("Error", "Failed to insert rental data.")
                        return
                    print(f"Inserted rental ID: {rental_id}")  # For debugging

                    # Decrease quantity available for the selected package
                    if not decrease_package_quantity(selected_package_id):
                        messagebox.showerror("Error", "Failed to update package quantity.")
                        return

                    # Fetch package price
                    package_price = fetch_package_price(selected_package_id)

                    if package_price is None:
                        messagebox.showerror("Error", "Failed to fetch package price.")
                        return

                    # Calculate total amount based on rental duration and package price
                    total_amount = rental_duration * package_price

                    # Format payment date
                    payment_date = datetime.now().strftime('%Y-%m-%d')

                    # Set payment status
                    payment_status = PaymentStatus.PENDING.value

                    # Print all values before insertion for debugging
                    print(
                        f"Inserting Payment with values: rental_id={rental_id}, payment_date={payment_date}, amount={total_amount}, payment_method={payment_method}, payment_status={payment_status}")

                    # Insert payment data into the database with rental_id
                    payment_id = insert_payment_to_db(rental_id, payment_date, total_amount, payment_method,
                                                      payment_status)

                    # Check if payment_id is None
                    if payment_id is None:
                        messagebox.showerror("Error", "Failed to insert payment data.")
                    else:
                        print(f"Inserted payment ID: {payment_id}")  # For debugging
                        messagebox.showinfo("Success", "Data saved successfully.")
                        clear_fields()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save data: {str(e)}")


            # SAVE BUTTON
            SaveButton = CTkButton(create_window, text="SAVE", font=('Century Gothic', 20, 'bold'), fg_color='#154734',
                                   text_color='white', hover_color='gray', corner_radius=10, command=submit_form)
            SaveButton.grid(row=2, column=0, padx=80, pady=20, sticky='e')

            # BACK BUTTON
            BackButton = CTkButton(create_window, text="CANCEL", font=('Century Gothic', 20, 'bold'),
                                   fg_color='#154734', text_color='white', hover_color='gray', corner_radius=10,
                                   command=BackRental)
            BackButton.grid(row=0, column=0, padx=25, pady=20, sticky='w')

            create_window.mainloop()

            # SAVE BUTTON
            SaveButton = CTkButton(create_window, text="SAVE", font=('Century Gothic', 20, 'bold'), fg_color='#154734',
                                   text_color='white', hover_color='gray', corner_radius=10,command=submit_form)
            SaveButton.grid(row=2, column=0, padx=50, pady=20, sticky='e')

            # BACK BUTTON
            BackButton = CTkButton(create_window, text="CANCEL", font=('Century Gothic', 20, 'bold'), fg_color='#154734',
                                   text_color='white', hover_color='gray', corner_radius=10, command=BackRental)
            BackButton.grid(row=0, column=0, padx=25, pady=20, sticky='w')

            create_window.mainloop()

        # Function to validate email format (Gmail only)
        def validate_email(email):
            # Gmail regex pattern
            pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@gmail.com$'
            return re.match(pattern, email)

        # Function to validate phone number (integer only)
        def validate_phone(phone):
            return phone.isdigit()

        # Function to open the update rental form for a selected customer
        def update_rental_window(customer_id):
            customer_data = fetch_customer_by_id(customer_id)

            if not customer_data:
                messagebox.showerror("Error", "Customer not found")
                return

            update_window = ctk.CTkToplevel()
            update_window.title("Update Rental")
            update_window.geometry("1100x700")
            update_window.configure(fg_color='#fefded')
            ctk.set_appearance_mode('light')
            update_window.grab_set()
            update_window.resizable(False, False)

            # MAIN FRAME
            frame1 = ctk.CTkScrollableFrame(update_window, fg_color='#f1f1f1', width=950, height=950)
            frame1.grid(row=1, column=0, padx=25, pady=25, sticky='nsew')

            update_window.grid_rowconfigure(1, weight=1)
            update_window.grid_columnconfigure(0, weight=1)

            # TITLE
            RentalForm = ctk.CTkLabel(frame1, text="Rental Form", text_color='#154734',
                                      font=('Century Gothic', 28, 'bold'))
            RentalForm.grid(row=0, column=0, padx=25, pady=10, sticky='w')

            # NAME
            CustNameLabel = ctk.CTkLabel(frame1, text="NAME:", text_color='black', font=('Century Gothic', 18, 'bold'))
            CustNameLabel.grid(row=1, column=0, padx=25, pady=10, sticky='w')
            CustName = ctk.CTkEntry(frame1, width=420, font=('Century Gothic', 18))
            CustName.grid(row=1, column=0, padx=90, pady=10, sticky='w')
            CustName.insert(0, f"{customer_data[1]} {customer_data[2]} {customer_data[3]}")

            # ADDRESS
            AddressLabel = ctk.CTkLabel(frame1, text="ADDRESS:", text_color='black',
                                        font=('Century Gothic', 18, 'bold'))
            AddressLabel.grid(row=2, column=0, padx=25, pady=10, sticky='w')
            Address = ctk.CTkEntry(frame1, width=400, font=('Century Gothic', 18))
            Address.grid(row=2, column=0, padx=110, pady=10, sticky='w')
            Address.insert(0, customer_data[4])

            # NUMBER
            PhoneLabel = ctk.CTkLabel(frame1, text="PHONE:", text_color='black', font=('Century Gothic', 18, 'bold'))
            PhoneLabel.grid(row=3, column=0, padx=25, pady=10, sticky='w')
            Phone = ctk.CTkEntry(frame1, width=410, font=('Century Gothic', 18))
            Phone.grid(row=3, column=0, padx=100, pady=10, sticky='w')
            Phone.insert(0, customer_data[5])

            # EMAIL
            EmailLabel = ctk.CTkLabel(frame1, text="EMAIL:", text_color='black', font=('Century Gothic', 18, 'bold'))
            EmailLabel.grid(row=4, column=0, padx=25, pady=10, sticky='w')
            Email = ctk.CTkEntry(frame1, width=410, font=('Century Gothic', 18))
            Email.grid(row=4, column=0, padx=100, pady=10, sticky='w')
            Email.insert(0, customer_data[6])


            def save_changes():
                # Validate email format
                if not validate_email(Email.get()):
                    messagebox.showerror("Error", "Invalid email format. Please enter a valid Gmail address.")
                    return

                # Validate phone number format
                if not validate_phone(Phone.get()):
                    messagebox.showerror("Error", "Phone number must contain digits only.")
                    return

                update_customer_in_db(customer_id, CustName.get(), '', '', Address.get(), Phone.get(), Email.get())
                update_window.destroy()  # Close the update window after saving changes

            # SAVE BUTTON
            UpdateButton = ctk.CTkButton(update_window, text="Save Changes", font=('Century Gothic', 21, 'bold'),
                                         fg_color='#154734', text_color='white', hover_color='gray', corner_radius=10,
                                         command=save_changes)
            UpdateButton.grid(row=2, column=0, padx=50, pady=20, sticky='e')

            def BackToRental():
                update_window.destroy()

            # BACK BUTTON
            Back2Button = ctk.CTkButton(update_window, text="BACK", font=('Century Gothic', 20, 'bold'),
                                        fg_color='#154734',
                                        text_color='white', hover_color='gray', corner_radius=10, command=BackToRental)
            Back2Button.grid(row=0, column=0, padx=25, pady=20, sticky='w')

            update_window.mainloop()
        def BackRental(booking_window):
            booking_window.withdraw()
            windows.deiconify()

        def BackToRental(updatebooking_window):
            updatebooking_window.withdraw()
            windows.deiconify()

        # Add Rental
        CreateRental = ctk.CTkButton(schedule_fm, text="CREATE", font=('Century Gothic', 21, 'bold'),
                                     fg_color='#154734', text_color='white', hover_color='gray',
                                     command=create_rental_window)
        CreateRental.grid(row=2, column=0, padx=1200, pady=10, sticky='w')


        def on_return_rental():
            try:
                selected_item = datagridview.selection()[0]  # Get the selected item
                values = datagridview.item(selected_item, "values")
                rental_id = values[0]
                package_id = values[3]

                # Call the return_rental function
                return_rental(rental_id, package_id)

                # Update the datagridview
                new_payment_status = "Paid"
                new_rental_status = "Returned"
                datagridview.set(selected_item, column="Payment Status", value=new_payment_status)
                datagridview.set(selected_item, column="Rental Status", value=new_rental_status)
            except IndexError:
                print("No item selected")

        # Button to return rental
        ReturnRental = ctk.CTkButton(schedule_fm, text="RETURN", font=('Century Gothic', 21, 'bold'),
                                     fg_color='#154734', text_color='white', hover_color='gray', command=on_return_rental)
        ReturnRental.grid(row=6, column=0, padx=1200, pady=10, sticky='w')

        # Custom style for ttk.Notebook
        style = ttk.Style()
        style.theme_use('default')

        # Notebook color and font customization
        style.configure('TNotebook', background='#fefded', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Century Gothic', 16, 'bold'), background='#154734', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#a3b18a'), ('active', 'gray')])

        # Style for Treeview rows
        style.configure("Treeview", font=('Century Gothic', 12))

        # Notebook for Tabs
        notebook = ttk.Notebook(schedule_fm, style='TNotebook')

        # Rental Tab
        RentalTab = ctk.CTkFrame(notebook, width=1355, height=600)
        notebook.add(RentalTab, text="Rental Tab")

        # Customer Tab
        CustomerTab = ctk.CTkFrame(notebook, width=1355, height=600)
        notebook.add(CustomerTab, text="Customer Tab")

        notebook.grid(row=5, column=0, columnspan=4, padx=50, pady=20, sticky='w')

        # Style for Headings
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Century Gothic', 13, 'bold'), background='#a3b18a',
                        foreground='black')

        def populate_treeview(datagridview, rows):
            for row in rows:
                datagridview.insert("", "end", values=row)


        # Data Grid View for Rental Tab
        datagridview = ttk.Treeview(RentalTab, columns=(
        "Rental ID", "Customer Name", "Package Price", "Package Name", "Rental Date", "Return Date", "Payment Status", "Rental Status"))
        datagridview.heading("#0", text="")
        datagridview.column("#0", width=0, stretch=NO)

        # Columns for Rental Tab
        datagridview.column("Rental ID", width=100, anchor='w')
        datagridview.heading("Rental ID", text="RENTAL ID")
        datagridview.column("Customer Name", width=250, anchor='w')
        datagridview.heading("Customer Name", text="CUSTOMER NAME")
        datagridview.column("Package Price", width=200, anchor='w')
        datagridview.heading("Package Price", text="PACKAGE PRICE")
        datagridview.column("Package Name", width=200, anchor='w')
        datagridview.heading("Package Name", text="PACKAGE NAME")
        datagridview.column("Rental Date", width=165, anchor='w')
        datagridview.heading("Rental Date", text="RENTAL DATE")
        datagridview.column("Return Date", width=165, anchor='w')
        datagridview.heading("Return Date", text="RETURN DATE")
        datagridview.column("Payment Status", width=160, anchor='w')
        datagridview.heading("Payment Status", text="PAYMENT STATUS")
        datagridview.column("Rental Status", width=150, anchor='w')
        datagridview.heading("Rental Status", text="RENTAL STATUS")


        datagridview.grid(row=0, column=0, sticky='nsew', columnspan=4)

        # Fetch data from the database and populate the Treeview
        rows = fetch_rental_data()
        populate_treeview(datagridview, rows)

        def populate_treeview(datagridview, rows):
            for row in rows:
                datagridview.insert("", "end", values=row)


        # Data Grid View for Customer Tab
        datagridview1 = ttk.Treeview(CustomerTab, columns=(
        "Customer ID", "Customer Name", "Address", "Contact Number", "Email Address", "Event Name", "Event Loc"))
        datagridview1.heading("#0", text="")
        datagridview1.column("#0", width=0, stretch=NO)

        # Columns for Customer Tab
        datagridview1.column("Customer ID", width=90, anchor='w')
        datagridview1.heading("Customer ID", text="CUST ID")
        datagridview1.column("Customer Name", width=210, anchor='w')
        datagridview1.heading("Customer Name", text="CUSTOMER NAME")
        datagridview1.column("Address", width=190, anchor='w')
        datagridview1.heading("Address", text="ADDRESS")
        datagridview1.column("Contact Number", width=250, anchor='w')
        datagridview1.heading("Contact Number", text="CONTACT NUMBER")
        datagridview1.column("Email Address", width=170, anchor='w')
        datagridview1.heading("Email Address", text="EMAIL ADDRESS")
        datagridview1.column("Event Name", width=250, anchor='w')
        datagridview1.heading("Event Name", text="EVENT NAME")
        datagridview1.column("Event Loc", width=230, anchor='w')
        datagridview1.heading("Event Loc", text="EVENT LOCATION")

        # Treeview grid for Customer Tab
        datagridview1.grid(row=0, column=0, sticky='nsew', columnspan=3)

        # Fetch data from the database and populate the Treeview
        rows = fetch_customer_data()
        populate_treeview(datagridview1, rows)

        # Bind double-click event for Customer Tab Treeview
        def on_treeview_double_click(event):
            item = datagridview1.identify('item', event.x, event.y)
            if item:
                customer_id = datagridview1.item(item, 'values')[0]
                update_rental_window(customer_id)

        datagridview1.bind('<Double-1>', on_treeview_double_click)