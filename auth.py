import sqlite3
import hashlib
import uuid

# Function to register a new user
def register_user(username, password):
    # Generate a unique salt for each user
    salt = uuid.uuid4().hex

    # Hash the password with the salt
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    # Store the salt and hashed password in the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, salt, is_admin, is_approved) VALUES (?, ?, ?, ?, ?)",
                   (username, hashed_password, salt, False, False))
    conn.commit()
    conn.close()

# Function to check if a user exists and the provided password is correct
def login_user(username, password):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT salt, password, is_admin, is_approved FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        salt, stored_password, is_admin, is_approved = user_data
        hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        if hashed_password == stored_password:
            return is_admin, is_approved
    return None, False

# Function to approve user registration by an admin
def approve_registration(username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_approved=? WHERE username=?", (True, username))
    conn.commit()
    conn.close()
