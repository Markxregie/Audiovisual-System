from tkinter import Tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
from rentalForm import Rental
from packageForm import Package
from equipmentForm import Equipment
from reportForm import Report
from paymentForm import Payment
from database_connection import fetch_total_rentals, fetch_total_pending_payments, fetch_monthly_earnings


class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard")
        self.master.geometry("1555x800")
        self.master.configure(bg="#fefded")
        self.master.resizable(False, False)
        self.active_button = None  # Track the currently active button

        # Initialize instance attributes
        self.option_frame = None
        self.main_frame = None
        self.photo_images = {}

        # Create widgets
        self.create_widgets()

    # Side Menu Frame
    def create_widgets(self):
        self.option_frame = ctk.CTkFrame(self.master, border_color='#D9D9D9', fg_color='#fefded', corner_radius=0,
                                         border_width=2)
        self.option_frame.pack(side=ctk.LEFT, fill=ctk.Y)

        # Load images
        self.load_images()

        # Print the current working directory for debugging
        print("Current working directory:", os.getcwd())



        # Option buttons
        self.create_button("home.png", self.homepage, 165, "home")
        self.create_button("rentals.png", self.rental, 227, "rentals")
        self.create_button("packages.png", self.package, 295, "packages")
        self.create_button("equipment.png", self.equipment, 359, "equipment")
        self.create_button("payments.png", self.payment, 420, "payments")
        self.create_button("reports.png", self.report, 490, "reports")
        self.create_button("logout.png", self.logout, 700, "logout")

        self.option_frame.pack_propagate(False)
        self.option_frame.configure(width=100, height=800 , corner_radius = 0)

        self.main_frame = ctk.CTkFrame(self.master, bg_color="#fefded", corner_radius=0)
        self.main_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(height=800, width=1490)

        self.homepage()

    def load_images(self):
        images = [
            ("home.png", (800, 800)),
            ("packages.png", (500, 500)),
            ("rentals.png", (500, 500)),
            ("equipment.png", (500, 500)),
            ("payments.png", (500, 500)),
            ("reports.png", (500, 500)),
            ("logout.png", (500, 500))
        ]

        for image_filename, size in images:
            image_path = os.path.join("Resources", image_filename)
            if os.path.exists(image_path):
                image = Image.open(image_path).resize(size, Image.LANCZOS)
                self.photo_images[image_filename] = CTkImage(dark_image=image)

    def create_logo(self, image_filename, y_pos):
        if image_filename in self.photo_images:
            # Ensure sufficient space in self.option_frame
            self.option_frame.configure(width=1600, height=1600)  # Adjust dimensions as needed

            logo_label = ctk.CTkLabel(self.option_frame, image=self.photo_images[image_filename], text="")
            logo_label.place(x=10, y=y_pos)

    def create_button(self, image_filename, command, y_pos, name):
        if image_filename in self.photo_images:
            button = ctk.CTkButton(self.option_frame, image=self.photo_images[image_filename], text="",
                                   fg_color="#fefded", border_width=0, hover_color="#A3B18A", width=95, height=50,
                                   command=lambda: self.on_button_click(name, command))
            button.place(x=2, y=y_pos)
            button.name = name
            setattr(self, f"{name}_button", button)
        else:
            print(f"Image {image_filename} not found in self.photo_images")

    def on_button_click(self, name, command):
        if self.active_button:
            self.active_button.configure(fg_color="#fefded")  # Reset the previous active button color

        # Set the new active button
        self.active_button = getattr(self, f"{name}_button")
        self.active_button.configure(fg_color="#A3B18A")  # Change the color of the clicked button
        command()

    # Homepage
    def homepage(self):

        self.clear_main_frame()

        homepage_fm = ctk.CTkFrame(self.main_frame, fg_color='#fefded')
        homepage_fm.pack(fill=ctk.BOTH, expand=True)

        header_frame = ctk.CTkFrame(homepage_fm, fg_color='#fefded')
        header_frame.pack(fill=ctk.X, pady=10, padx=20)

        homepage_lb = ctk.CTkLabel(header_frame, text='Dashboard', font=('Century Gothic', 42, 'bold'),
                                   text_color='#154734')
        homepage_lb.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        datetime_label = ctk.CTkLabel(header_frame, text="", font=('Century Gothic', 20), text_color='#154734')
        datetime_label.grid(row=0, column=0, padx=1100, pady=20, sticky='e')

        header_frame.columnconfigure(1, weight=1)

        # Update Time
        def update_time():
            now = datetime.now()
            formatted_time = now.strftime("%A: %B %d, %Y, %I:%M %p")
            datetime_label.configure(text=formatted_time)
            homepage_fm.after(1000, update_time)

        update_time()

        container_frame = ctk.CTkFrame(homepage_fm, fg_color='#fefded')
        container_frame.pack(pady=20, padx=20, anchor='n', fill=ctk.X)

        left_frame = ctk.CTkFrame(container_frame, fg_color='#fefded')
        left_frame.pack(pady=10, padx=10, anchor='n', side='left', fill=ctk.Y, expand=True)

        # Plotting the bar graph
        earnings_frame = ctk.CTkFrame(container_frame, fg_color='#fefded', corner_radius=5, width=1000, height=700)
        earnings_frame.pack(pady=40, padx=0, anchor='n', side='right', fill=ctk.X, expand=True)
        earnings_frame.pack_propagate(False)

        earnings_label = ctk.CTkLabel(earnings_frame, text='Earnings', font=('Century Gothic bold', 35),
                                      text_color='#154734')
        earnings_label.pack(pady=6, padx=20, anchor='w')

        fig, ax = plt.subplots(figsize=(10, 3))
        fig.patch.set_facecolor('#fefded')
        ax.set_facecolor('#fefded')

        earnings_data = fetch_monthly_earnings()
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


        # Plot the bar graph with black text annotations above each bar
        bars = ax.bar(labels, earnings_data, color='#154734')

        # Annotate each bar with its value (black color, bold font, above the bar)
        for bar, value in zip(bars, earnings_data):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'₱{value}', ha='center', va='bottom', color='black',
                    fontweight='bold')

        ax.set_title('Monthly Earnings', color='#154734')
        ax.set_xlabel('Month', color='#154734')
        ax.set_ylabel('Earnings', color='#154734')
        ax.tick_params(axis='x', colors='#154734')
        ax.tick_params(axis='y', colors='#154734')

        canvas = FigureCanvasTkAgg(fig, master=earnings_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        #Total of rentals
        rentals_frame = ctk.CTkFrame(left_frame, fg_color='#F1F1F1', corner_radius=20, height= 700, width=300)
        rentals_frame.pack(pady=10, padx=10, anchor='n', side='left', fill=ctk.Y, expand=True)
        rentals_frame.pack_propagate(False)

        rentals_label = ctk.CTkLabel(rentals_frame, text='TOTAL RENTALS', font=('Century Gothic bold', 24),text_color='#154734')
        rentals_label.pack(pady=30, padx=20, anchor='w')

        total_rentals = fetch_total_rentals()
        if total_rentals is not None:
            total_rentals_label = ctk.CTkLabel(rentals_frame, text=str(total_rentals), font=('Century Gothic bold', 30),
                                               fg_color='#F1F1F1', text_color='#154734')
            total_rentals_label.pack(pady=35, padx=100, anchor='w')
        else:
            total_rentals_label = ctk.CTkLabel(rentals_frame, text="Error fetching data",
                                               font=('Century Gothic bold', 15),
                                               fg_color='#F1F1F1', text_color='#154734')
            total_rentals_label.pack(pady=35, padx=100, anchor='w')


        #Pending payments
        pending_payments_label = ctk.CTkLabel(rentals_frame, text='PENDING PAYMENTS', font=('Century Gothic bold', 24),text_color='#154734')
        pending_payments_label.pack(pady=20, padx=20, anchor='sw')

        # Fetch total pending payments
        total_pending_payments = fetch_total_pending_payments()

        # Display total pending payments count or error message if fetch fails
        if total_pending_payments is not None:
            pending_payments_value_label = ctk.CTkLabel(rentals_frame, text=str(total_pending_payments), font=('Century Gothic bold', 30), fg_color='#F1F1F1', text_color='#154734')
            pending_payments_value_label.pack(pady=15, padx=100, anchor='w')
        else:
            pending_payments_value_label = ctk.CTkLabel(rentals_frame, text="Error fetching data", font=('Century Gothic bold', 15), fg_color='#F1F1F1', text_color='#154734')
            pending_payments_value_label.pack(pady=15, padx=100, anchor='w')



    # CALLING THE PAGES
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def rental(self):
        self.clear_main_frame()
        Rental(self.main_frame)

    def package(self):
        self.clear_main_frame()
        Package(self.main_frame)

    def equipment(self):
        self.clear_main_frame()
        Equipment(self.main_frame)

    def payment(self):
        self.clear_main_frame()
        Payment(self.main_frame)

    def report(self):
        self.clear_main_frame()
        Report(self.main_frame)

    def logout(self):
        self.master.destroy()
        pass

    def switch(self, page_function):
        self.clear_main_frame()
        page_function()


