import tkinter as tk
from tkinter import messagebox
import auth  # Import the authentication module

# Function to handle user login
def login():
    username = entry_username.get()
    password = entry_password.get()

    is_admin, is_approved = auth.login_user(username, password)

    if is_admin:
        messagebox.showinfo("Login Successful", "Logged in as admin.")
        # You can redirect to the admin panel or perform admin-specific actions here.
    elif is_approved:
        messagebox.showinfo("Login Successful", "Logged in as a regular user.")
        # You can redirect to the user panel or perform user-specific actions here.
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to open the registration window
def open_registration():
    registration_window = tk.Toplevel(root)
    registration_window.title("User Registration")

    label_username = tk.Label(registration_window, text="Username")
    label_password = tk.Label(registration_window, text="Password")

    entry_new_username = tk.Entry(registration_window, width=30)
    entry_new_password = tk.Entry(registration_window, width=30, show="*")

    label_username.grid(row=0, column=0)
    entry_new_username.grid(row=0, column=1)
    label_password.grid(row=1, column=0)
    entry_new_password.grid(row=1, column=1)

    def register_new_user():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        auth.register_user(new_username, new_password)
        messagebox.showinfo("Registration Complete", "Your registration request has been sent for approval.")

    register_button = tk.Button(registration_window, text="Register", command=register_new_user)
    register_button.grid(row=2, column=0, columnspan=2)

# Create the main login window
root = tk.Tk()
root.title("User Login")

label_username = tk.Label(root, text="Username")
label_password = tk.Label(root, text="Password")

entry_username = tk.Entry(root, width=30)
entry_password = tk.Entry(root, width=30, show="*")

label_username.grid(row=0, column=0)
entry_username.grid(row=0, column=1)
label_password.grid(row=1, column=0)
entry_password.grid(row=1, column=1)

login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2)

register_button = tk.Button(root, text="Register", command=open_registration)
register_button.grid(row=3, column=0, columnspan=2)

root.mainloop()
