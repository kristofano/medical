import tkinter as tk
import mysql.connector

# Create a Tkinter window
root = tk.Tk()
root.title("Desktop Application")

# Create a function to connect to MySQL and retrieve data
def fetch_data():
    # Replace with your MySQL database credentials
    conn = mysql.connector.connect(
        host="localhost",
        user="kris",
        password="1234",
        database="pacjenci"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")
    data = cursor.fetchall()
    
    for item in data:
        result_label.config(text=item)

    conn.close()

# Create a button to fetch data from MySQL
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.pack()

# Create a label to display the fetched data
result_label = tk.Label(root, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()