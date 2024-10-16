from tkinter import Tk
from Login import LoginWindow
from dasboard import Dashboard
from database_connection import initialize_database

def main():
    # Initialize the database and create tables
    #initialize_database()

    # Initialize loginwindow
    root = Tk()
    login_window = LoginWindow(root)
    root.mainloop()

    # After login is successful go to dashboard
    if login_window.login_successful:
        root = Tk()
        app = Dashboard(root)
        root.mainloop()

if __name__ == "__main__":
    main()
