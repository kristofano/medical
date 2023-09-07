import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import auth  # Import the authentication module
import hashlib
import uuid

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the "patients" table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                  patient_id INTEGER PRIMARY KEY,
                  pesel INTEGER,
                  first_name TEXT,
                  last_name TEXT,
                  age INTEGER,
                  gender TEXT,
                  diagnosis TEXT
                )''')

# Close the database connection when done
conn.close()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Create the "users" table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  salt TEXT NOT NULL,
                  is_admin BOOLEAN DEFAULT 0,
                  is_approved BOOLEAN DEFAULT 0
                )''')

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

# Function to validate a 9-digit PESEL number
def is_valid_pesel(pesel):
    return len(pesel) == 11 and pesel.isdigit()

# Function to calculate age from PESEL
def calculate_age_from_pesel(pesel):
    try:
        birth_year = int(pesel[0:2])
        birth_month = int(pesel[2:4])
        birth_day = int(pesel[4:6])

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        age = current_year - (1900 + birth_year)

        if birth_month > current_month or (birth_month == current_month and birth_day > current_day):
            age -= 1

        return age
    except:
        return None

# Function to validate the gender input
def is_valid_gender(gender):
    return gender in ["M", "K", "I"]

# Function to add a new patient
def add_patient():
    def save_patient():
        # Get data from the entry widgets
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        pesel = entry_pesel.get()
        gender = entry_gender.get()
        diagnosis = entry_diagnosis.get()

        if not is_valid_pesel(pesel):
            messagebox.showerror("Invalid PESEL", "PESEL number must be exactly 11 digits.")
            return

        if not is_valid_gender(gender):
            messagebox.showerror("Invalid Gender", "Gender must be 'M' (male), 'K' (female), or 'I' (other).")
            return

        # Insert the patient data into the database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (first_name, last_name, pesel, gender, diagnosis) VALUES (?, ?, ?, ?, ?)",
                       (first_name, last_name, pesel, gender, diagnosis))
        conn.commit()
        conn.close()

        messagebox.showinfo("Patient Added", "Patient data has been added successfully.")
        add_patient_window.destroy()
        refresh_table()

    # Create a new window for adding a patient
    add_patient_window = tk.Toplevel(root)
    add_patient_window.title("Add New Patient")

    # Create entry widgets for entering patient information
    entry_first_name = tk.Entry(add_patient_window, width=30)
    entry_last_name = tk.Entry(add_patient_window, width=30)
    entry_pesel = tk.Entry(add_patient_window, width=30)
    entry_gender = tk.Entry(add_patient_window, width=30)
    entry_diagnosis = tk.Entry(add_patient_window, width=30)

    # Create labels for the entry widgets
    label_first_name = tk.Label(add_patient_window, text="First Name")
    label_last_name = tk.Label(add_patient_window, text="Last Name")
    label_pesel = tk.Label(add_patient_window, text="PESEL")
    label_gender = tk.Label(add_patient_window, text="Gender")
    label_diagnosis = tk.Label(add_patient_window, text="Diagnosis")

    # Create a button to save the patient data
    save_button = tk.Button(add_patient_window, text="Save", command=save_patient)

    # Place widgets in the add patient window
    label_first_name.grid(row=0, column=0)
    entry_first_name.grid(row=0, column=1)
    label_last_name.grid(row=1, column=0)
    entry_last_name.grid(row=1, column=1)
    label_pesel.grid(row=2, column=0)
    entry_pesel.grid(row=2, column=1)
    label_gender.grid(row=3, column=0)
    entry_gender.grid(row=3, column=1)
    label_diagnosis.grid(row=4, column=0)
    entry_diagnosis.grid(row=4, column=1)
    save_button.grid(row=5, column=0, columnspan=2)

# Function to edit patient data
def edit_patient():
    def save_edited_patient():
        # Get data from the entry widgets
        updated_first_name = entry_first_name.get()
        updated_last_name = entry_last_name.get()
        updated_pesel = entry_pesel.get()
        updated_gender = entry_gender.get()
        updated_diagnosis = entry_diagnosis.get()

        if not is_valid_pesel(updated_pesel):
            messagebox.showerror("Invalid PESEL", "PESEL number must be exactly 11 digits.")
            return

        if not is_valid_gender(updated_gender):
            messagebox.showerror("Invalid Gender", "Gender must be 'M' (male), 'K' (female), or 'I' (other).")
            return

        # Update the patient data in the database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET first_name=?, last_name=?, pesel=?, gender=?, diagnosis=? WHERE patient_id=?",
                       (updated_first_name, updated_last_name, updated_pesel, updated_gender, updated_diagnosis, selected_patient_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Patient Updated", "Patient data has been updated successfully.")
        edit_patient_window.destroy()
        refresh_table()

    # Get the selected patient's data from the selected row
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient to edit.")
        return

    selected_patient_id = tree.item(selected_item, "values")[0]

    # Create a new window for editing a patient
    edit_patient_window = tk.Toplevel(root)
    edit_patient_window.title("Edit Patient")

    # Retrieve the patient's data from the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, pesel, gender, diagnosis FROM patients WHERE patient_id=?", (selected_patient_id,))
    patient_data = cursor.fetchone()
    conn.close()

    # Create entry widgets for editing patient information
    entry_first_name = tk.Entry(edit_patient_window, width=30)
    entry_last_name = tk.Entry(edit_patient_window, width=30)
    entry_pesel = tk.Entry(edit_patient_window, width=30)
    entry_gender = tk.Entry(edit_patient_window, width=30)
    entry_diagnosis = tk.Entry(edit_patient_window, width=30)

    # Create labels for the entry widgets
    label_first_name = tk.Label(edit_patient_window, text="First Name")
    label_last_name = tk.Label(edit_patient_window, text="Last Name")
    label_pesel = tk.Label(edit_patient_window, text="PESEL")
    label_gender = tk.Label(edit_patient_window, text="Gender")
    label_diagnosis = tk.Label(edit_patient_window, text="Diagnosis")

    # Set the entry widgets with the retrieved patient data
    entry_first_name.insert(0, patient_data[0])
    entry_last_name.insert(0, patient_data[1])
    entry_pesel.insert(0, patient_data[2])
    entry_gender.insert(0, patient_data[3])
    entry_diagnosis.insert(0, patient_data[4])

    # Create a button to save the edited patient data
    save_button = tk.Button(edit_patient_window, text="Save", command=save_edited_patient)

    # Place widgets in the edit patient window
    label_first_name.grid(row=0, column=0)
    entry_first_name.grid(row=0, column=1)
    label_last_name.grid(row=1, column=0)
    entry_last_name.grid(row=1, column=1)
    label_pesel.grid(row=2, column=0)
    entry_pesel.grid(row=2, column=1)
    label_gender.grid(row=3, column=0)
    entry_gender.grid(row=3, column=1)
    label_diagnosis.grid(row=4, column=0)
    entry_diagnosis.grid(row=4, column=1)
    save_button.grid(row=5, column=0, columnspan=2)

# Function to delete a patient
def delete_patient():
    # Get the selected patient's data from the selected row
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient to delete.")
        return

    selected_patient_id = tree.item(selected_item, "values")[0]

    # Confirm the deletion with a dialog
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this patient?")
    if not confirm:
        return

    # Delete the patient data from the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id=?", (selected_patient_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Patient Deleted", "Patient data has been deleted successfully.")
    refresh_table()

# Function to refresh the patient data table
def refresh_table():
    # Clear the current data in the table
    for row in tree.get_children():
        tree.delete(row)

    # Retrieve and insert the updated data from the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT patient_id, first_name, last_name, pesel, gender, diagnosis FROM patients")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        patient_id, first_name, last_name, pesel, gender, diagnosis = row
        age = calculate_age_from_pesel(pesel)
        tree.insert("", "end", values=(patient_id, first_name, last_name, pesel, age, gender, diagnosis))

# Create the main application window
root = tk.Tk()
root.title("Patient Management System")

# Create a Treeview widget to display patient data
tree = ttk.Treeview(root, columns=("Patient ID", "First Name", "Last Name", "PESEL", "Age", "Gender", "Diagnosis"))
tree.heading("#1", text="Patient ID")
tree.heading("#2", text="First Name")
tree.heading("#3", text="Last Name")
tree.heading("#4", text="PESEL")
tree.heading("#5", text="Age")
tree.heading("#6", text="Gender")
tree.heading("#7", text="Diagnosis")
tree.pack()

# Create buttons to add, edit, and delete patients
add_patient_button = tk.Button(root, text="Add Patient", command=add_patient)
edit_patient_button = tk.Button(root, text="Edit Patient", command=edit_patient)
delete_patient_button = tk.Button(root, text="Delete Patient", command=delete_patient)
refresh_button = tk.Button(root, text="Refresh", command=refresh_table)

add_patient_button.pack()
edit_patient_button.pack()
delete_patient_button.pack()
refresh_button.pack()

# Start the Tkinter main loop
refresh_table()
root.mainloop()
