import tkinter as tk
from tkinter import ttk, messagebox
from app.customer.customer_controller import CustomerController
import re

class CustomersView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        
        # Initialize the controller with a reference to self
        self.controller = CustomerController(self)
        
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)
        
        self.is_edit_mode = False  # Track whether we're in "edit" mode
        self.current_customer_id = None  # Track room being edited
        
      
        
        # Left Frame (30%) - Room Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()
        
        # Right Frame (70%) - Room List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)
        
        # Initialize data view but do not load data yet
        self.create_data_view()
        

    # Form
    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Customer", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Customer Name
        tk.Label(self.form_frame, text="Name:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.name_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.name_entry.pack(fill="x", pady=10, ipady=5)

        # Customer Email
        tk.Label(self.form_frame, text="Email:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.email_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.email_entry.pack(fill="x", pady=10, ipady=5)

        # Customer Phone
        tk.Label(self.form_frame, text="Phone:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.phone_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.phone_entry.pack(fill="x", pady=10, ipady=5)

        # Customer Address
        tk.Label(self.form_frame, text="Address:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.address_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.address_entry.pack(fill="x", pady=10, ipady=5)

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Customer", font=("Helvetica", 14, "bold"), 
            bg=self.primary_color, fg="white", relief="flat", command=self.handle_add_or_update, cursor="hand2"
        )
        self.add_button.pack(pady=20, fill="x", ipady=5)

        # Cancel Button (initially hidden)
        self.cancel_button = tk.Button(
            self.form_frame, text="Cancel", font=("Helvetica", 12),
            bg="grey", fg="white", relief="flat", command=self.reset_form, cursor="hand2"
        )
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.cancel_button.pack_forget()

    def handle_add_or_update(self):
        customer_name = self.name_entry.get()
        customer_email = self.email_entry.get()
        customer_phone = self.phone_entry.get()
        customer_address = self.address_entry.get()
        
        # Validate email
        if not self.validate_email(customer_email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Validate phone number
        if not self.validate_phone(customer_phone):
            messagebox.showerror("Invalid Phone Number", "Please enter a valid 11-digit phone number.")
            return
        if customer_address == "" or customer_name == "":
            messagebox.showerror("Invalid Entry", "Please fill all fields")
            return

        if self.is_edit_mode:
            # Update customer
            self.controller.update_customer(self.current_customer_id, customer_name, customer_email, customer_phone, customer_address)
            self.reset_form()
        else:
            # Add new customer
            self.controller.add_customer(customer_name, customer_email, customer_phone, customer_address)
            messagebox.showinfo("Success", "New Customer added successfully.")
    def reset_form(self):
        """ Resets the form to add mode and clears entries """
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.add_button.config(text="Add Customer")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_customer_id = None
        
    def create_data_view(self):
        # Search Bar Frame
        search_frame = tk.Frame(self.data_frame, bg="white")
        search_frame.pack(fill="x", pady=10)
        
        # Search Label and Entry
        tk.Label(search_frame, text="Search:", bg="white", font=("Helvetica", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)
        
        # Search Button
        self.search_button = tk.Button(
            search_frame, text="Search", command=self.handle_search, 
            bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"), cursor="hand2"
        )
        self.search_button.pack(side="left", padx=5)

        # Customer List Table, including "actions" in columns
        self.customer_list = ttk.Treeview(self.data_frame, columns=("Id","name", "email", "phone", "address", "actions"), show="headings")
        self.customer_list.heading("Id", text="Customer Id")
        self.customer_list.heading("name", text="Name")
        self.customer_list.heading("email", text="Email")
        self.customer_list.heading("phone", text="Phone")
        self.customer_list.heading("address", text="Address")
        self.customer_list.heading("actions", text="Actions")

        # Set column widths and center-align
        for col in ("Id","name", "email", "phone", "address"):
            self.customer_list.column(col, anchor="center", width=80)
        self.customer_list.column("actions", anchor="center", width=150)  # Extra space for actions

        # Bind single-click event for action handling
        self.customer_list.bind("<Button-1>", self.on_single_click)

        # Pack customer list table
        self.customer_list.pack(fill="both", expand=True, pady=10)

        # Load all data on page load
        self.update_customer_list(self.controller.get_all_customers())

    def handle_search(self):
        keyword = self.search_entry.get()
        customers = self.controller.search_customers(keyword)
        self.update_customer_list(customers)

    def update_customer_list(self, customers):
        # Clear current data in customer list
        for i in self.customer_list.get_children():
            self.customer_list.delete(i)

        # Insert new data into customer list with action labels as text
        for customer in customers:
            customer_id = customer['Id']  # Assuming the customer data contains 'Id'
            self.customer_list.insert("", "end", values=(customer['Id'],customer['name'], customer['email'], customer['phone'], customer['address'], "Edit | Delete"), iid=customer_id)

    def on_single_click(self, event):
        # Identify the row and column where the click occurred
        item_id = self.customer_list.identify_row(event.y)
        column_id = self.customer_list.identify_column(event.x)

        if item_id and column_id == '#6':  # '#6' corresponds to the "actions" column
            # Retrieve customer_id from item_id directly
            customer_id = item_id

            # Get the x-coordinate within the actions column to determine if "Edit" or "Delete" was clicked
            x_offset = event.x - self.customer_list.bbox(item_id, column_id)[0]

            # Assuming "Edit" is on the left half and "Delete" on the right half of the actions cell
            if x_offset < 75:  # Approximate midpoint of 150 width
                customer_data = self.customer_list.item(item_id, "values")
                self.initiate_edit(customer_id, customer_data)
            else:
                self.delete_customer(customer_id)  # Use customer_id for deletion

    def initiate_edit(self, customer_id, customer_data):
        self.current_customer_id = customer_id
        self.is_edit_mode = True
        self.add_button.config(text="Update Customer")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        # Populate form fields
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, customer_data[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, customer_data[2])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer_data[3])
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, customer_data[4])

    def delete_customer(self, customer_id):
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this room?")
        if response:
            # customer_id = customer_data[0]
            print(customer_id)
            self.controller.delete_customer(customer_id)
            self.controller.refresh_customer_list() 

   