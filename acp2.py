import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        # Set the window to fullscreen
        self.root.attributes('-fullscreen', True)

        # Load the background image
        self.bg_image = tk.PhotoImage(file="C:/Users/Isabella/Documents/NetbeansProjects/jnfvdkj/login_.png")  # Replace with your image path

        # Create a Canvas for the background
        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Add the image to the Canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create the frame on top of the background
        self.frame = tk.Frame(self.root, bg='#0e1013', bd=10)
        self.frame.place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.6, anchor='center')

        # Username Label and Entry
        self.username_label = tk.Label(self.frame, text="Username:", font=("Bahnschrift SemiBold Condensed", 18), fg="white", bg='#0e1013')
        self.username_label.grid(row=0, column=0, padx=35, pady=10)

        self.username_entry = tk.Entry(self.frame, font=("Bahnschrift SemiBold Condensed", 18), bd=2)
        self.username_entry.grid(row=0, column=1, padx=35, pady=10)

        # Password Label and Entry
        self.password_label = tk.Label(self.frame, text="Password:", font=("Bahnschrift SemiBold Condensed", 18), fg="white", bg='#0e1013')
        self.password_label.grid(row=1, column=0, padx=50, pady=30)

        self.password_entry = tk.Entry(self.frame, font=("Bahnschrift SemiBold Condensed", 18), bd=2, show='*')
        self.password_entry.grid(row=1, column=1, padx=50, pady=30)

        # Checkbox to show/hide password
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(
            self.frame, text="Show Password", variable=self.show_password_var, bg='#0e1013', fg='white',
            font=("Bahnschrift SemiBold Condensed", 15), command=self.toggle_password_visibility
        )
        self.show_password_checkbox.grid(row=2, column=1, padx=20, pady=10)

        # Login Button
        self.login_button = tk.Button(self.frame, text="Login", font=("Bahnschrift SemiBold Condensed", 18), bg='red', fg='white', border= '5px solid red',command=self.login)
        self.login_button.grid(row=3, column=0, padx=30, columnspan=3, pady=25,sticky="e",) 

        # Exit Button
        self.exit_button = tk.Button(self.frame, text="Exit", font=("Bahnschrift SemiBold Condensed", 18), bg='grey', fg='black', border= '5px solid grey',command=self.root.quit)
        self.exit_button.grid(row=3, column=1,padx=30, columnspan=3, pady=25, sticky="w",)

    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def login(self):
        """Handle login functionality."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password")
            return

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="03182005Elola",  # Update your database password
                database="marjodb"
            )

            cursor = connection.cursor()
            query = "SELECT * FROM admintable WHERE BINARY username = %s AND BINARY password = %s"
            cursor.execute(query, (username, password))

            result = cursor.fetchone()  # Fetch one record
            if result:
                messagebox.showinfo("Login Successful", "Welcome!")
                self.root.withdraw()  # Hide the login window
                MainApp(tk.Toplevel(self.root))  # Create a new window for the main app
            else:
                messagebox.showerror("Invalid Credentials", "Invalid Username or Password")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.root.attributes('-fullscreen', True)

        # File path to the image
        image_path = "C:/Users/Isabella/Documents/NetbeansProjects/jnfvdkj/login_.png"

        try:
            # Load the background image and store it as an attribute
            self.bg_image = tk.PhotoImage(file=image_path)
        except tk.TclError:
            # If the image can't be loaded, show an error message and exit
            messagebox.showerror("Error", f"Image file not found or invalid: {image_path}")
            self.root.destroy()  # Close the application
            return

        # Create a Canvas for the background
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Add the image to the Canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create buttons directly on the canvas
        self.button_inventory = tk.Button(
            self.root,
            text="Manage Inventory",
            command=self.show_inventory_frame,
            font=("Consulas ", 16),
            bg="#588773",
            fg="#ffffff",
            width=15,
            border= '5px solid white',
        )
        self.button_order = tk.Button(
            self.root,
            text=" Manage  Orders ",
            command=self.show_order_frame,
            font=("Consulas", 16),
            bg="#588773",
            fg="#ffffff",
            width=15,
            border= '5px solid white',
        )
        # Create the exit button with canvas.create_window
        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            font=("Consulas", 16),
            bg='grey',
            fg='#ffffff',
            border='5px solid grey',
            command=self.root.quit
        )

        # Add exit button to canvas
        self.canvas.create_window(750, 480, anchor="center", window=self.exit_button)  # Adjust position as needed
        # Add buttons to the canvas with proper alignment
        self.canvas.create_window(750, 320, anchor="center", window=self.button_inventory)
        self.canvas.create_window(750, 400, anchor="center", window=self.button_order)

        # Create frames for inventory and order management but don't pack them yet
        self.inventory_frame = InventoryApp(self.root, self)  # Instantiate InventoryApp
        self.order_frame = ManageOrderApp(self.root, self)  # Correctly instantiate ManageOrderApp

    def show_inventory_frame(self):
        """Show the inventory management frame."""
        self.canvas.pack_forget()  # Hide the main menu canvas
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)  # Show the inventory frame

    def show_order_frame(self):
        """Show the order management frame."""
        self.canvas.pack_forget()  # Hide the main menu canvas
        self.order_frame.refresh_inventory_table()  # Refresh the inventory table
        self.order_frame.pack(fill=tk.BOTH, expand=True)  # Show the order fram

    def go_back_home(self):
        """Return to the main menu."""
        self.inventory_frame.pack_forget()  # Hide inventory frame
        self.order_frame.pack_forget()  # Hide order frame
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Show main menu frame
        # Call refresh_inventory_table on the correct instance
        self.inventory_frame.refresh_table()
        self.order_frame.refresh_inventory_table()

class InventoryApp(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent, bg='#0e1013')  # Use parent instead of root
        self.main_app = main_app  # Reference to the main app for back navigation
        self.create_widgets()
        self.create_database_connection()
        self.refresh_table()

    def create_widgets(self):
        # Title Label
        self.label_title = tk.Label(self, text="FOOD STOCK", font=("Arial Black", 25, 'bold'), fg="#ff0000", bg='#0e1013')  # Use self instead of self.root
        self.label_title.pack(pady=20)

        # Frame for the table
        self.frame = tk.Frame(self, bg="gray")  # Use self instead of self.root
        self.frame.pack(pady=20, padx=90, fill=tk.BOTH, expand=True)

        # Inventory Table
        self.inventory_table = ttk.Treeview(self.frame, columns=("ID", "Name", "Quantity", "Price", "Category"), show='headings', height=10)
        self.inventory_table.heading("ID", text="ID")
        self.inventory_table.heading("Name", text="Name")
        self.inventory_table.heading("Quantity", text="Quantity")
        self.inventory_table.heading("Price", text="Price")
        self.inventory_table.heading("Category", text="Category")

        self.inventory_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.inventory_table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventory_table.configure(yscrollcommand=self.scrollbar.set)

        # Entry Fields Frame
        self.entry_frame = tk.Frame(self, bg="#0e1013")  # Use self instead of self.root
        self.entry_frame.pack(pady=10)

        # Modern Entry and Label Design
        self.create_label_entry(self.entry_frame, "ID:", 0, 0, width=10, readonly=True)
        self.create_label_entry(self.entry_frame, "Name:", 1, 0, width=20)
        self.create_label_entry(self.entry_frame, "Quantity:", 2, 0, width=20)
        self.create_label_entry(self.entry_frame, "Price:", 3, 0, width=20)
        self.create_label_entry(self.entry_frame, "Category:", 4, 0, width=20)

        # Buttons Frame
        self.button_frame = tk.Frame(self, bg="#0e1013")  # Use self instead of self.root
        self.button_frame.pack(pady=20)

        # Modern Buttons
        self.create_button(self.button_frame, "Add", self.save_item, 0, 0)
        self.create_button(self.button_frame, "Update", self.update_item, 0, 1)
        self.create_button(self.button_frame, "Delete", self.delete_item, 0, 2)

        # Back to Home Button
        self.back_button = tk.Button(self, text="Back to Home", command=self.go_back_home, font=("Segoe UI", 12), bg="#e74c3c", fg="#ffffff", relief="flat")  # Use self instead of self.root
        self.back_button.pack(anchor="se")

        # Bind table item selection
        self.inventory_table.bind("<ButtonRelease-1>", self.select_item)
        self.bind("<Button-1>", self.deselect_item_if_needed)

    def create_label_entry(self, parent, label_text, row, col, width=20, readonly=False):
        """Helper function to create a label and entry with modern style and alignment."""
        label = tk.Label(parent, text=label_text, font=("Segoe UI", 12), fg="#e6c223", bg="#0e1013")
        label.grid(row=row, column=col, padx=10, pady=5, sticky="e")  # Align labels to the right

        entry = tk.Entry(parent, font=("Segoe UI", 12), width=width, bd=2, relief="solid", fg="#34495e", bg='#f5f5f5')
        if readonly:
            entry.config(state='readonly')
        entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")  # Align entries to the left

        # Dynamically create entry attributes for later access
        setattr(self, f"entry_{label_text.strip(':').lower()}", entry)


    def create_button(self, parent, text, command, row, col):
        """Helper function to create buttons with modern style."""
        button = tk.Button(parent, text=text, font=("Segoe UI", 12), command=command, bg="#3498db", fg="#ffffff",
                           width=12, relief="flat", bd=0)
        button.grid(row=row, column=col, padx=10, pady=10)
        button.config(activebackground="#2980b9", activeforeground="#ffffff")

    def create_database_connection(self):
        """Create the DB connection and ensure the table exists."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user="root", password="03182005Elola", database="marjodb"
            )
            self.cursor = self.conn.cursor()

            # Ensure that the inventory table exists
            self.cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS inventoryTable (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    price DECIMAL(10, 2),
                    quantity INT,
                    category VARCHAR(100)
                );
            """)
            self.conn.commit()

            # Reset the AUTO_INCREMENT if necessary (ensure no gaps)
            self.reset_auto_increment()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to the database: {err}")
            self.root.quit()

    def reset_auto_increment(self):
        """Resets the AUTO_INCREMENT value to the next available ID."""
        self.cursor.execute("SELECT MAX(id) FROM inventoryTable")
        max_id = self.cursor.fetchone()[0]
        if max_id is not None:
            self.cursor.execute(f"ALTER TABLE inventoryTable AUTO_INCREMENT = {max_id + 1}")
            self.conn.commit()

    def save_item(self):
        """Save a new item to the inventory."""
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        category = self.entry_category.get()

        if not name or not quantity or not price or not category:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be an integer and Price must be a number.")
            return

        try:
            # Check if the item already exists in the inventory
            self.cursor.execute("SELECT id FROM inventoryTable WHERE name = %s", (name,))
            existing_item = self.cursor.fetchone()

            if existing_item:
                messagebox.showwarning("Duplicate Item", f"The item '{name}' already exists in the inventory.")
                return

            # Insert the new item into the database if it doesn't already exist
            self.cursor.execute("INSERT INTO inventoryTable (name, quantity, price, category) VALUES (%s, %s, %s, %s)",
                                (name, quantity, price, category))
            self.conn.commit()
            messagebox.showinfo("Success", "Item saved successfully.")
            self.clear_inputs()
            self.refresh_table()
            self.main_app.order_frame.refresh_inventory_table()  # Corrected here

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error saving the item: {err}")
        
    def update_item(self):
        """Update an existing item in the inventory."""
        item_id = self.entry_id.get()
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        category = self.entry_category.get()

        if not item_id or not name or not quantity or not price or not category:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        try:
            item_id = int(item_id)
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "ID must be an integer, Quantity must be an integer, and Price must be a number.")
            return

        try:
            # Update the item in the database by ID
            self.cursor.execute("UPDATE inventoryTable SET name=%s, quantity=%s, price=%s, category=%s WHERE id=%s",
                                (name, quantity, price, category, item_id))
            self.conn.commit()
            self.main_app.order_frame.refresh_inventory_table()  # Call refresh_inventory_table here
            messagebox.showinfo("Success", "Item updated successfully.")
            self.clear_inputs()
            self.refresh_table()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating the item: {err}")

    def delete_item(self):
        """Delete an item from the inventory."""
        # Make sure the entry_id is editable so that we can access its value
        self.entry_id.config(state='normal')
        
        item_id = self.entry_id.get()

        if not item_id:
            messagebox.showwarning("Input Error", "Select an item to delete.")
            return

        try:
            item_id = int(item_id)  # Convert the item_id to an integer
        except ValueError:
            messagebox.showwarning("Input Error", "ID must be an integer.")
            return

        try:
            # Delete the item from the database by ID
            self.cursor.execute("DELETE FROM inventoryTable WHERE id=%s", (item_id,))
            self.conn.commit()

            # Reset AUTO_INCREMENT value to avoid skipping IDs after deletion
            self.reset_auto_increment()

            messagebox.showinfo("Success", "Item deleted successfully.")

            self.clear_inputs()
            self.refresh_table()
            self.main_app.order_frame.refresh_inventory_table()  # Corrected here
            self.main_app.order_frame.inventory_table.update_idletasks()  # Add this line
            
            # Set the entry_id field back to readonly after the deletion
            self.entry_id.config(state='readonly')

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting the item: {err}")
        

    def refresh_table(self):
        """Refresh the inventory table to show updated data."""
        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        self.cursor.execute("SELECT * FROM inventoryTable")
        rows = self.cursor.fetchall()
        for row in rows:
            self.inventory_table.insert("", "end", values=row)

    def deselect_item_if_needed(self, event):
        """Deselect the row if clicked outside the table area."""
        # Check if click happened outside the inventory table
        if self.inventory_table.identify_region(event.x, event.y) == "nothing":
            self.clear_inputs()

    def select_item(self, event):
        """Select an item from the table and fill the entry fields."""
        selected_item = self.inventory_table.focus()
        item_details = self.inventory_table.item(selected_item)['values']

        if item_details:
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, item_details[0])  # This will show the ID
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, item_details[1])
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, item_details[2])
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, item_details[3])
            self.entry_category.delete(0, tk.END)
            self.entry_category.insert(0, item_details[4])
            self.entry_id.config(state='readonly')  # Set ID as read-only again

    def clear_inputs(self):
        """Clear input fields."""
        self.entry_id.config(state='normal')  # Allow editing the ID field
        self.entry_id.delete(0, tk.END)  # Clear the ID field
        self.entry_id.config(state='readonly')  # Set ID field back to read-only

        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)


    def go_back_home(self):
        """Return to the main menu."""
        self.pack_forget()  # Hide inventory frame
        self.main_app.canvas.pack(fill=tk.BOTH, expand=True)  # Show main menu frame
        self.main_app.order_frame.refresh_inventory_table()  # Ref
        

    def __del__(self):
        """Clean up the database connection when the object is destroyed."""
        if hasattr(self, 'db_connection'):
            self.db_connection.close()


class ManageOrderApp(tk.Frame):
    
    def __init__(self, parent, main_app):
        super().__init__(parent, bg="#000000")  # Set background color to black
        self.main_app = main_app  # Reference to the main app for back navigation
        self.create_widgets()
        self.create_database_connection()
        self.refresh_inventory_table()

        # Initialize order data
        self.order_items = []  # Will store tuples of (item_id, item_name, item_price, item_quantity)
        self.total_amount = 0.0  # Initialize total amount
        self.selected_item = None  # Track selected item 

    def create_widgets(self):
        # Title Label
        self.label_title = tk.Label(self, text="MANAGE ORDER", font=("Arial Black", 25, 'bold'), fg="red", bg="#000000")
        self.label_title.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Frame for the two-column layout
        self.frame_main = tk.Frame(self, bg="#000000")
        self.frame_main.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        # Ensure that both columns in the main frame are evenly spaced
        self.frame_main.grid_columnconfigure(0, weight=1)  # Left side space
        self.frame_main.grid_columnconfigure(1, weight=2)  # Center space for table
        self.frame_main.grid_columnconfigure(2, weight=1)  # Right side space

        # Top Section: Inventory Table (Occupies the center space)
        self.frame_inventory = tk.Frame(self.frame_main, bg="#000000")
        self.frame_inventory.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        # Inventory Table
        self.inventory_table = ttk.Treeview(self.frame_inventory, columns=("ID", "Name", "Quantity", "Price", "Category"), show='headings', height=10)
        self.inventory_table.heading("ID", text="ID")
        self.inventory_table.heading("Name", text="Name")
        self.inventory_table.heading("Quantity", text="Quantity")
        self.inventory_table.heading("Price", text="Price")
        self.inventory_table.heading("Category", text="Category")

        # Adjust font and background for the table
        self.inventory_table.tag_configure('dark', background='#000000', foreground='#ffffff')
        self.inventory_table.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.frame_inventory, orient="vertical", command=self.inventory_table.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.inventory_table.configure(yscrollcommand=self.scrollbar.set)

        # Bind the treeview selection event to capture the selected item
        self.inventory_table.bind('<<TreeviewSelect>>', self.on_item_select)

        # Bottom Section: Order List and Controls
        self.frame_bottom = tk.Frame(self, bg="#000000")
        self.frame_bottom.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        # Left Column - Order Items Listbox
        self.frame_left = tk.Frame(self.frame_bottom, bg="#000000")
        self.frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label_order_list = tk.Label(self.frame_left, text="Order Items", font=("Segoe UI", 14, 'bold'), fg="#ffffff", bg="#000000")
        self.label_order_list.grid(row=0, column=0, pady=10)

        self.order_listbox = tk.Listbox(self.frame_left, font=("Segoe UI", 12), height=4, width=40, bd=2, relief="solid", bg="#2c3e50", fg="#ffffff")
        self.order_listbox.grid(row=1, column=0, pady=10, sticky="nsew")

        # Right Column - Controls
        self.frame_right = tk.Frame(self.frame_bottom, bg="#000000")
        self.frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Ensure that both columns in the right section are evenly spaced
        self.frame_right.grid_columnconfigure(0, weight=1, uniform="equal")
        self.frame_right.grid_columnconfigure(1, weight=1, uniform="equal")

        # Entry Fields Frame
        self.entry_frame = tk.Frame(self.frame_right, bg="#000000")
        self.entry_frame.grid(row=0, column=0, pady=10)

        self.create_label_entry(self.entry_frame, "Quantity:", 0, 0, width=10)

        # Add Item, Complete Order, and Back buttons
        self.button_frame = tk.Frame(self.frame_right, bg="#000000")
        self.button_frame.grid(row=1, column=0, pady=20)

        self.create_button(self.button_frame, "Add to Order", self.add_to_order, 0, 0)
        self.create_button(self.button_frame, "Complete Order", self.complete_order, 0, 1)
        self.create_button(self.button_frame, "Back to Home", self.go_back_home, 0, 2)

        # Order Summary Frame
        self.order_summary_frame = tk.Frame(self.frame_right, bg="#000000")
        self.order_summary_frame.grid(row=2, column=0, pady=10, sticky="ew")

        # Label for Selected Item
        self.label_selected_item = tk.Label(self.order_summary_frame, text="Selected Item: None", font=("Segoe UI", 12), fg="#ffffff", bg="#000000")
        self.label_selected_item.grid(row=0, column=0, columnspan=2, sticky="w", padx=10)

        # Label for Total
        self.label_total = tk.Label(self.order_summary_frame, text="Total: ₱0.00", font=("Segoe UI", 14), fg="LightGreen", bg="#000000")
        self.label_total.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

        # Label for Amount Paid
        self.label_paid = tk.Label(self.order_summary_frame, text="Amount Paid: ₱", font=("Segoe UI", 14), fg="Red", bg="#000000")
        self.label_paid.grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

        # Entry for Amount Paid
        self.entry_paid = tk.Entry(self.order_summary_frame, font=("Segoe UI", 12), width=10, bd=2, relief="solid", fg="#34495e", bg="#ecf0f1")
        self.entry_paid.grid(row=2, column=1, pady=5, sticky="w", padx=10)

        # Label for Change
        self.label_change = tk.Label(self.order_summary_frame, text="Change: ₱0.00", font=("Segoe UI", 14), fg="White", bg="#000000")
        self.label_change.grid(row=3, column=0, columnspan=2, sticky="w", pady=5, padx=10)

        # Bind event to update the change when the amount paid changes
        self.entry_paid.bind("<KeyRelease>", self.update_change)

        # Adjust grid configurations for the parent frames
        self.order_summary_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.order_summary_frame.grid_columnconfigure(1, weight=1, uniform="equal")

    def create_label_entry(self, parent, label_text, row, col, width=20):
        label = tk.Label(parent, text=label_text, font=("Segoe UI", 12), fg="#ffffff", bg="#000000")
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

        entry = tk.Entry(parent, font=("Segoe UI", 12), width=width, bd=2, relief="solid", fg="#ffffff", bg="#34495e")
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        setattr(self, f"entry_{label_text.strip(':').lower()}", entry)

    def create_button(self, parent, text, command, row, col):
        button = tk.Button(parent, text=text, font=("Segoe UI", 12), command=command, bg="#3498db", fg="#ffffff", width=12, relief="flat", bd=0)
        button.grid(row=row, column=col, padx=10, pady=10)
        button.config(activebackground="#2980b9", activeforeground="#ffffff")

    def create_database_connection(self):
        """Create a MySQL database connection."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="03182005Elola",  # Ensure the password is correct
                database="marjodb"
            )
            self.cursor = self.conn.cursor()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to the database: {err}")
            self.master.quit()

    def refresh_inventory_table(self):
        """Populate the inventory table with available items."""
        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        try:
            self.cursor.execute("SELECT * FROM inventoryTable")
            rows = self.cursor.fetchall()
            for row in rows:
                self.inventory_table.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data from the database: {err}")
            

    def on_item_select(self, event):
        # Get the selected item details and update the UI
        selected_item = self.inventory_table.focus()
        if selected_item:
            item_details = self.inventory_table.item(selected_item)
            item_name = item_details['values'][1]
            item_price = item_details['values'][3]
            self.selected_item = (item_name, item_price)
            self.label_selected_item.config(text=f"Selected Item: {item_name} ({item_price})")
    
    def add_to_order(self):
        # Add the selected item to the order listbox
        if self.selected_item:
            item_name, item_price = self.selected_item
            item_quantity = self.entry_quantity.get()
            if item_quantity.isdigit() and int(item_quantity) > 0:
                item_quantity = int(item_quantity)
                self.order_items.append((item_name, item_price, item_quantity))
                self.order_listbox.insert(tk.END, f"{item_name} x{item_quantity} - ₱{float(item_price) * item_quantity:.2f}")
                self.update_total()
                self.entry_quantity.delete(0, tk.END)  # Clear the quantity entry field
            else:
                # Handle invalid quantity input
                tk.messagebox.showerror("Invalid Input", "Please enter a valid quantity.")

    def update_total(self):
        self.total_amount = sum([float(item[1]) * item[2] for item in self.order_items])
        self.label_total.config(text=f"Total: ₱{self.total_amount:.2f}")
    
    def complete_order(self):
        # Handle the order completion logic
        if self.total_amount == 0:
            tk.messagebox.showwarning("No items", "Please add items to the order.")
            return
        
        # Get the amount paid
        try:
            amount_paid = float(self.entry_paid.get())
            if amount_paid < self.total_amount:
                tk.messagebox.showwarning("Insufficient Payment", "Amount paid is less than the total.")
                return
            change = amount_paid - self.total_amount
            self.label_change.config(text=f"Change: ₱{change:.2f}")
            # Reset after completing the order
            self.clear_order()
        except ValueError:
            tk.messagebox.showerror("Invalid Payment", "Please enter a valid amount paid.")

    def clear_order(self):
        # Clear the order list and reset the UI
        self.order_items.clear()
        self.order_listbox.delete(0, tk.END)
        self.entry_paid.delete(0, tk.END)
        self.label_selected_item.config(text="Selected Item: None")
        self.label_total.config(text="Total: ₱0.00")
        self.label_change.config(text="Change: ₱0.00")



    def update_change(self, event):
        # Calculate change as the amount paid is updated
        try:
            amount_paid = float(self.entry_paid.get())
            if amount_paid >= self.total_amount:
                change = amount_paid - self.total_amount
                self.label_change.config(text=f"Change: ₱{change:.2f}")
            else:
                self.label_change.config(text="Change: ₱0.00")
        except ValueError:
            self.label_change.config(text="Change: ₱0.00")


    def go_back_home(self):
        """Return to the main menu."""
        self.pack_forget()  # Hide order frame
        self.main_app.canvas.pack(fill=tk.BOTH, expand=True)
        
    def __del__(self):
        """Clean up the database connection when the object is destroyed."""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)  # Show the login screen first
    root.mainloop()