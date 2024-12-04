import tkinter as tk
from tkinter import messagebox
import subprocess  # To run another Python script (dashboard.py)
from mysql_connector import connect_to_database, check_password

def validate_login(username, password):
    """Fetch user data and validate login credentials."""
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()  # Fetch the user's record

        if user:
            # Validate the hashed password
            if check_password(password, user['password']):
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
                return False
        else:
            messagebox.showerror("Login Failed", "Username not found.")
            return False
    except Exception as e:
        print(f"Error during login validation: {e}")
        messagebox.showerror("Login Failed", "An error occurred during login.")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def on_login():
    """Handle login button click."""
    username = username_entry.get()
    password = password_entry.get()

    if validate_login(username, password):
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def open_dashboard():
    """Open the dashboard.py script when login is successful."""
    subprocess.run(["python", "dashboard.py"])

def on_exit():
    """Exit the application."""
    root.quit()

# Set up the main application window
root = tk.Tk()
root.title("Login")
root.geometry("400x300")

# Create labels and input fields for username and password
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)

username_entry = tk.Entry(root)
username_entry.pack(pady=10)

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=10)

password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=10)

# Create login button
login_button = tk.Button(root, text="Login", command=on_login)
login_button.pack(pady=20)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(pady=10)

# Start the application
root.mainloop()
