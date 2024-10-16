import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from database_connection import fetch_payment_data

class Payment(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.main_frame = ctk.CTkFrame(self.master)

        payments_fm = ctk.CTkFrame(self.master, fg_color='#fefded')
        payments_fm.pack(fill='both', expand=True)

        # Payments label
        payments_lb = ctk.CTkLabel(payments_fm, text="Payments", font=('Century Gothic', 30, 'bold'),
                                   text_color='#154734')
        payments_lb.grid(row=0, column=0, padx=40, pady=20, sticky='w')

        # Function to update the time
        def updateTime():
            now = datetime.now()
            formatted_time = now.strftime("%A: %B %d, %Y, %I:%M%p")
            DateTime.configure(text=formatted_time)
            payments_fm.after(1000, updateTime)

        # DateTime label
        DateTime = ctk.CTkLabel(payments_fm, text="", font=('Century Gothic', 20, 'bold'), text_color='#154734')
        DateTime.grid(row=0, column=1, padx=860, pady=20, sticky='w')
        updateTime()

        # Custom style for ttk.Notebook
        style = ttk.Style()
        style.theme_use('default')

        # Style for headings
        style.configure("Treeview.Heading", font=('Century Gothic', 13, 'bold'), background='#a3b18a',
                        foreground='black')

        # Style for Treeview rows
        style.configure("Treeview", font=('Century Gothic', 12))

        # Frame for data grid view
        frame_payments = ctk.CTkFrame(payments_fm, fg_color='#fefded')
        frame_payments.grid(row=1, column=0, columnspan=2, sticky='w', padx=20, pady=20)

        def populate_treeview(datagridview, rows):
            for row in rows:
                datagridview.insert("", "end", values=row)

        # Data grid view for rental tab
        datagridview_payments = ttk.Treeview(frame_payments, columns=(
        "Rental ID", "Customer Name", "Total Amount", "Package Name", "Rental Start", "Return Date", "Payment Status" , "Payment Method"))
        datagridview_payments.heading("#0", text="")
        datagridview_payments.column("#0", width=10, stretch=ctk.NO)

        # Columns for rental tab
        datagridview_payments.column("Rental ID", width=100, anchor='w')
        datagridview_payments.heading("Rental ID", text="RENTAL ID")
        datagridview_payments.column("Customer Name", width=280, anchor='w')
        datagridview_payments.heading("Customer Name", text="CUSTOMER NAME")
        datagridview_payments.column("Total Amount", width=150, anchor='w')
        datagridview_payments.heading("Total Amount", text="TOTAL AMOUNT")
        datagridview_payments.column("Package Name", width=220, anchor='w')
        datagridview_payments.heading("Package Name", text="PACKAGE NAME")
        datagridview_payments.column("Rental Start", width=170, anchor='w')
        datagridview_payments.heading("Rental Start", text="RENTAL START")
        datagridview_payments.column("Return Date", width=170, anchor='w')
        datagridview_payments.heading("Return Date", text="RETURN DATE")
        datagridview_payments.column("Payment Status", width=150, anchor='w')
        datagridview_payments.heading("Payment Status", text="PAYMENT STATUS")
        datagridview_payments.column("Payment Method", width=160, anchor='w')
        datagridview_payments.heading("Payment Method", text="PAYMENT METHOD")

        datagridview_payments.grid(row=0, column=0, sticky='nsew')

        # Fetch data from the database and populate the Treeview
        rows = fetch_payment_data()
        populate_treeview(datagridview_payments, rows)

        # Configure grid row and column to expand
        frame_payments.grid_rowconfigure(0, weight=1)
        frame_payments.grid_columnconfigure(0, weight=1)
