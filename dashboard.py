import tkinter as tk
from tkinter import ttk

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("600x400")  # Adjusted size for better layout

        # Creating a frame for the buttons on the left side
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Create Buttons to Switch Tabs
        self.create_buttons()

        # Creating the Notebook widget to handle tab switching
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="right", fill="both", expand=True)

        # Creating the tabs (frames)
        self.accounts_frame = ttk.Frame(self.notebook)
        self.qc_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.accounts_frame, text="ACCOUNTS")
        self.notebook.add(self.qc_frame, text="QC")
        self.notebook.add(self.dashboard_frame, text="DASHBOARD")

    def create_buttons(self):
        """Create the buttons to switch between tabs."""
        # Button to show ACCOUNTS tab
        accounts_button = tk.Button(self.button_frame, text="ACCOUNTS", width=20, command=lambda: self.switch_tab(self.accounts_frame))
        accounts_button.pack(pady=10)

        # Button to show QC tab
        qc_button = tk.Button(self.button_frame, text="QC", width=20, command=lambda: self.switch_tab(self.qc_frame))
        qc_button.pack(pady=10)

        # Button to show DASHBOARD tab
        dashboard_button = tk.Button(self.button_frame, text="DASHBOARD", width=20, command=lambda: self.switch_tab(self.dashboard_frame))
        dashboard_button.pack(pady=10)

    def switch_tab(self, frame):
        """Switch the current tab to the specified frame."""
        self.notebook.select(frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
