import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from datetime import datetime
from database_connection import fetch_package_equipment


class Package(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.main_frame = ctk.CTkFrame(self.master)

        package_fm = ctk.CTkFrame(self.master, fg_color='#fefded')
        package_fm.pack(fill='both', expand=True)

        package_lbl = ctk.CTkLabel(package_fm, text="Package", font=('Century Gothic', 30, 'bold'),
                                   text_color='#154734')
        package_lbl.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        # Function to update the time
        def updateTime():
            now = datetime.now()
            formatted_time = now.strftime("%A, %B %d, %Y, %I:%M %p")
            DateTime.configure(text=formatted_time)
            package_fm.after(1000, updateTime)

        # DateTime label
        DateTime = ctk.CTkLabel(package_fm, text="", font=('Century Gothic', 20, 'bold'), text_color='#154734')
        DateTime.grid(row=0, column=1, padx=20, pady=20, sticky='e')  # Adjusted column position
        updateTime()

        # Scrollable frame
        frame1 = ctk.CTkScrollableFrame(package_fm, fg_color='#f1f1f1', width=1400, height=700)
        frame1.grid(row=2, column=0, padx=20, pady=40, sticky='w')

        # Call method to display package equipment information
        self.display_package_equipment(frame1)

    def display_package_equipment(self, frame1):
        rows = fetch_package_equipment()

        for row in rows:
            package_label = ctk.CTkLabel(frame1, text=f"Package ID: {row[0]}, Package Name: {row[1]}",
                                         font=('Century Gothic', 22, 'bold'), text_color='#154734')
            package_label.pack(anchor='w', padx=20)

            included_label = ctk.CTkLabel(frame1, text=f"Included Equipment: {row[2]}", font=('Century Gothic', 18))
            included_label.pack(anchor='w', padx=20)

            separator = ttk.Separator(frame1, orient='horizontal')
            separator.pack(fill='x', pady=20)

