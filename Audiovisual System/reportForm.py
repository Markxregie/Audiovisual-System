import customtkinter as ctk
from datetime import datetime
from tkinter import ttk
from database_connection import fetch_returned_rentals, soft_delete_rental
from tkinter import messagebox

class Report(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.main_frame = ctk.CTkFrame(self.master)
        self.create_widgets()

    def create_widgets(self):
        # Main frame for reports
        report_fm = ctk.CTkFrame(self.master, fg_color='#fefded')
        report_fm.pack(fill='both', expand=True)

        # Report label
        payments_lb = ctk.CTkLabel(report_fm, text="Archives", font=('Century Gothic', 30, 'bold'), text_color='#154734')
        payments_lb.grid(row=0, column=0, padx=40, pady=20, sticky='w')

        # DateTime label
        self.DateTime = ctk.CTkLabel(report_fm, text="", font=('Century Gothic', 20), text_color='#154734')
        self.DateTime.grid(row=0, column=2, padx=70, pady=20, sticky='e')

        # Custom style for ttk.Notebook
        style = ttk.Style()
        style.theme_use('default')
        # STYLE FOR HEADINGS
        style.configure("Treeview.Heading", font=('Century Gothic', 13, 'bold'), background='#a3b18a',
                        foreground='black')

        # Function to populate the Treeview
        def populate_treeview(treeview, data):
            for row in data:
                treeview.insert('', 'end', values=row)

        # Function to refresh or populate the Treeview with updated data
        def refresh_treeview():
            # Fetch updated data
            returned_rentals = fetch_returned_rentals()
            # Clear existing items in Treeview
            datagridview.delete(*datagridview.get_children())
            # Populate Treeview with updated data
            populate_treeview(datagridview, returned_rentals)

        # Function to handle double-click event
        def on_double_click(event):
            selected_item = datagridview.selection()[0]
            rental_id = datagridview.item(selected_item)['values'][0]

            # Show confirmation dialog
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Rental ID {rental_id}?")
            if confirm:
                soft_delete_rental(rental_id)
                refresh_treeview()

        # DATA GRID VIEW FOR AVAILABLE TAB
        datagridview = ttk.Treeview(report_fm,
                                    columns=("Rental ID", "Customer ID", "Event ID", "Payment ID", "Customer Name", "Rental Date", "Return Date", "Rental Status"))
        datagridview.heading("#0", text="")
        datagridview.column("#0", width=0, stretch="no")

        # COLUMNS FOR AVAILABLE TAB
        datagridview.column("Rental ID", width=100, anchor='w')
        datagridview.heading("Rental ID", text="RENTAL ID")
        datagridview.column("Customer ID", width=100, anchor='w')
        datagridview.heading("Customer ID", text="CUST ID")
        datagridview.column("Event ID", width=100, anchor='w')
        datagridview.heading("Event ID", text="EVENT ID")
        datagridview.column("Payment ID", width=100, anchor='w')
        datagridview.heading("Payment ID", text="PAYMENT ID")
        datagridview.column("Customer Name", width=250, anchor='w')
        datagridview.heading("Customer Name", text="CUSTOMER NAME")
        datagridview.column("Rental Date", width=250, anchor='w')
        datagridview.heading("Rental Date", text="RENTAL DATE")
        datagridview.column("Return Date", width=250, anchor='w')
        datagridview.heading("Return Date", text="RETURN DATE")
        datagridview.column("Rental Status", width=200, anchor='w')
        datagridview.heading("Rental Status", text="RENTAL STATUS")

        datagridview.grid(row=2, padx=20, pady=20, column=0, sticky='nw', columnspan=3)

        # Fetch and populate the Treeview with data
        returned_rentals = fetch_returned_rentals()
        populate_treeview(datagridview, returned_rentals)

        # Bind double-click event to perform soft delete
        datagridview.bind("<Double-1>", on_double_click)
        # Function to update the time
        def updateTime():
            now = datetime.now()
            formatted_time = now.strftime("%A, %B %d, %Y, %I:%M %p")
            self.DateTime.configure(text=formatted_time)
            self.main_frame.after(1000, updateTime)

        updateTime()
