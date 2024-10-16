import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import hashlib
from dasboard import Dashboard
from tkinter import Label

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1555x800")
        self.root.configure(bg="#A3B18A")
        self.root.resizable(False, False)
        self.login_successful = False
        self.configure_ui()

    # Configure UI for Login Page
    def configure_ui(self):
        self.label = Label(self.root, text="Login Window", font=("Arial", 24), fg="#A3B18A", bg="#A3B18A")
        self.label.pack(pady=20)

        self.central_background_frame = ctk.CTkFrame(self.root, width=1500, height=750, corner_radius=32, fg_color="#B5C1A1")
        self.central_background_frame.place(relx=0.5, rely=0.5, anchor='center')

        login_frame = ctk.CTkFrame(self.root, width=360, height=500, corner_radius=32, fg_color="#FEFDED", bg_color="#B5C1A1")
        login_frame.place_configure(width=400, height=490, relx=0.5, rely=0.5, anchor='center')


        # Load and resize the logo image
        logo_image_path = r"C:\Users\user\Documents\LAST\Resources\testinglogo1.png"
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((255, 170))

        # Create a CTkImage instance
        self.logo_photo = ctk.CTkImage(logo_image, size=(200, 160))

        self.logo_label = ctk.CTkLabel(master=login_frame, image=self.logo_photo, text="")
        self.logo_label.grid(row=0, column=0, padx=100, pady=(20, 5))

        # Username and password entry
        self.name_label = ctk.CTkLabel(master=login_frame, text="NAME", font=("DM sans", 14), text_color="black")
        self.name_label.grid(row=1, column=0, padx=70, pady=(0, 0), sticky="w")

        self.name_entry = ctk.CTkEntry(master=login_frame, width=270, height=35, fg_color="#D9D9D9", border_color="#D9D9D9", corner_radius=10,)
        self.name_entry.grid(row=2, column=0, padx=0, pady=5)

        self.password_label = ctk.CTkLabel(master=login_frame, text="PASSWORD", font=("DM sans", 14), text_color="black")
        self.password_label.grid(row=3, column=0, padx=70, pady=(10, 5), sticky="w")

        self.password_entry = ctk.CTkEntry(master=login_frame, width=270, height=35, font=("DM sans", 14), text_color="black", fg_color="#D9D9D9", border_color="#D9D9D9", corner_radius=10, show="*")
        self.password_entry.grid(row=4, column=0, padx=20, pady=5)

        # Login button
        self.login_button = ctk.CTkButton(master=login_frame, text="Log in", font=("DM sans", 14, "bold"), width=150, height=35, fg_color="#154734", hover_color="#588157", command=self.login)
        self.login_button.grid(row=5, column=0, padx=20, pady=(20, 10))

    #Function For Hashing
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.name_entry.get()
        password = self.password_entry.get()
        hashed_password = self.hash_password(password)

        # Dummy check for username and hashed password
        if username == "admin" and hashed_password == self.hash_password("admin"):
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_dashboard(self):
        self.root.destroy()
        root = ctk.CTk()
        app = Dashboard(root)
        root.mainloop()
