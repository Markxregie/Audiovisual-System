import customtkinter as ctk
from customtkinter import *
from tkinter import ttk
from datetime import datetime
from database_connection import fetch_available_packages, fetch_rented_packages

class Equipment(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.main_frame = ctk.CTkFrame(self.master)
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.master, fg_color='#fefded', height=800)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Ensure the main frame expands to fill the space
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Date and Time update function
        def updateTime():
            now = datetime.now()
            formatted_time = now.strftime("%A: %B %d, %Y, %I:%M%p")
            self.DateTime.configure(text=formatted_time)
            self.main_frame.after(1000, updateTime)

        # Title
        rentals = ctk.CTkLabel(self.main_frame, text="Inventory", font=('Century Gothic', 30, 'bold'),
                               text_color='#154734')
        rentals.grid(row=0, column=0, padx=40, pady=20, sticky='w')

        self.DateTime = ctk.CTkLabel(self.main_frame, text="", font=('Century Gothic', 20, 'bold'),
                                     text_color='#154734')
        self.DateTime.grid(row=0, column=0, padx=1100, pady=20, sticky='w')
        updateTime()

        # Custom style for ttk.Notebook
        style = ttk.Style()
        style.theme_use('default')

        # Notebook color and font customization
        style.configure('TNotebook', background='#fefded', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Century Gothic', 16, 'bold'), background='#154734', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#a3b18a'), ('active', 'gray')])

        # Style for Treeview rows
        style.configure("Treeview", font=('Century Gothic', 12))

        # NOTEBOOK FOR TABS
        notebook = ttk.Notebook(self.main_frame, style='TNotebook')

        # AVAILABLE TAB
        AvailableTab = CTkFrame(notebook, width=1450, height=600)
        notebook.add(AvailableTab, text="Available")

        # RENTED TAB
        RentedTab = CTkFrame(notebook, width=1450, height=600)
        notebook.add(RentedTab, text="Rented")

        notebook.grid(row=3, column=0, columnspan=2, padx=70, pady=20, sticky='w')

        # STYLE FOR HEADINGS
        style.configure("Treeview.Heading", font=('Century Gothic', 13, 'bold'), background='#a3b18a',
                        foreground='black')

        def populate_treeview(datagridview, rows):
            for row in rows:
                datagridview.insert("", "end", values=row)

        # DATA GRID VIEW FOR AVAILABLE TAB
        datagridview = ttk.Treeview(AvailableTab,
                                    columns=("Package ID", "Package Name", "Rental Price", "Quantity"))
        datagridview.heading("#0", text="")
        datagridview.column("#0", width=0, stretch="no")

        # COLUMNS FOR AVAILABLE TAB
        datagridview.column("Package ID", width=250, anchor='w')
        datagridview.heading("Package ID", text="PACKAGE ID")
        datagridview.column("Package Name", width=450, anchor='w')
        datagridview.heading("Package Name", text="PACKAGE NAME")
        datagridview.column("Rental Price", width=300, anchor='w')
        datagridview.heading("Rental Price", text="RENTAL PRICE")
        datagridview.column("Quantity", width=300, anchor='w')
        datagridview.heading("Quantity", text="QUANTITY")

        datagridview.grid(row=0, column=0, sticky='nsew', columnspan=3)

        # Fetch data from the database and populate the Treeview
        rows = fetch_available_packages()
        populate_treeview(datagridview, rows)

        def populate_treeview(datagridview, rows):
            for row in rows:
                datagridview.insert("", "end", values=row)

        # Data grid for rented tab
        datagridview1 = ttk.Treeview(RentedTab,
                                     columns=("Package ID", "Package Name", "Rental Price", "Total Rented"))
        datagridview1.heading("#0", text="")
        datagridview1.column("#0", width=0, stretch="no")

        # Columns for rented tab
        datagridview1.column("Package ID", width=250, anchor='w')
        datagridview1.heading("Package ID", text="PACKAGE ID")
        datagridview1.column("Package Name", width=450, anchor='w')
        datagridview1.heading("Package Name", text="PACKAGE NAME")
        datagridview1.column("Rental Price", width=300, anchor='w')
        datagridview1.heading("Rental Price", text="RENTAL PRICE")
        datagridview1.column("Total Rented", width=300, anchor='w')
        datagridview1.heading("Total Rented", text="TOTAL RENTED")

        # Fetch data and populate Treeview
        rented_packages = fetch_rented_packages()
        populate_treeview(datagridview1, rented_packages)

        datagridview1.grid(row=0, column=0, sticky='nsew', columnspan=3)