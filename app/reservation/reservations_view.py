import tkinter as tk
from tkcalendar import DateEntry 
from tkinter import ttk, messagebox
from tkinter import ttk, messagebox
from app.reservation.reservation_controller import ReservationController
from app.reservation.reservation_model import ReservationModel
from datetime import datetime


class ReservationsView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False
        self.current_reservation_id = None  # Track reservation being edited

        # Initialize the controller with a reference to self
        self.controller = ReservationController(self)

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)
        
        # Fetch all customer IDs and room IDs for dropdowns
        room_model = ReservationModel()
        self.room_options =room_model.fetch_rooms()  
        
        self.room_ids = [room['Id'] for room in self.room_options]
      
        
        
        # Fetch all customer IDs for dropdown
        customer_model = ReservationModel()
        raw_customer_ids = customer_model.fetch_customer_ids()  # Fetch all customer IDs as list of numbers
        # self.customer_options = [f"Customer ID - {customer_id}" for customer_id in raw_customer_ids]
        self.customer_options = raw_customer_ids
        
        # Title
        tk.Label(
            self.frame, text="Reservation Management Section", bg=secondary_color, 
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Reservation Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Reservation List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)
        
        # Initialize data view but do not load data yet
        self.create_data_view()

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Reservation", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

         # Room ID (Dropdown)
        tk.Label(self.form_frame, text="Room ID:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.room_id_var = tk.StringVar()
        self.room_id_var.set(self.room_ids[0] if self.room_ids else "No rooms available")  # Set default value
        self.room_id_entry = tk.OptionMenu(self.form_frame, self.room_id_var, *self.room_ids)
        self.room_id_entry.config(font=("Helvetica", 14))
        self.room_id_entry.pack(fill="x", pady=10, ipady=5)

        # # Customer ID (Dropdown)
        # tk.Label(self.form_frame, text="Customer ID:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        # self.customer_id_var = tk.StringVar()
        # self.customer_id_var.set(self.customer_options[0])  # Set default value
        # self.customer_id_entry = tk.OptionMenu(self.form_frame, self.customer_id_var, *self.customer_options)
        # self.customer_id_entry.config(font=("Helvetica", 14))
        # self.customer_id_entry.pack(fill="x", pady=4, ipady=5)
         # Customer ID (Searchable Dropdown using ttk.Combobox)
        tk.Label(self.form_frame, text="Customer ID:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")

        self.customer_id_var = tk.StringVar()
        self.customer_id_var.set(self.customer_options[0])  # Set default value
        
        # Create a combobox for the customer ID dropdown (Searchable)
        self.customer_id_entry = ttk.Combobox(self.form_frame, textvariable=self.customer_id_var, values=self.customer_options, state="normal", font=("Helvetica", 14), width=30)
        self.customer_id_entry.set(self.customer_options[0])  # Set default value
        self.customer_id_entry.pack(fill="x", pady=4, ipady=5)

        # Check-In Date and Time
        tk.Label(self.form_frame, text="Check-In Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.checkin_entry = DateEntry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid", date_pattern="yyyy-mm-dd")
        self.checkin_entry.pack(fill="x", pady=5, ipady=5)

        # Check-Out Date and Time
        tk.Label(self.form_frame, text="Check-Out Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.checkout_entry = DateEntry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid", date_pattern="yyyy-mm-dd")
        self.checkout_entry.pack(fill="x", pady=5, ipady=5)

        # Status
        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.status_entry.pack(fill="x", pady=5, ipady=5)

        # Total Amount
        # tk.Label(self.form_frame, text="Total Amount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        # self.total_amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        # self.total_amount_entry.pack(fill="x", pady=10, ipady=5)

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Reservation", font=("Helvetica", 14, "bold"), 
            bg=self.primary_color, fg="white", relief="flat", command=self.handle_add_or_update, cursor="hand2"
        )
        self.add_button.pack(pady=5, fill="x", ipady=5)

        # Cancel Button (initially hidden)
        self.cancel_button = tk.Button(
            self.form_frame, text="Cancel", font=("Helvetica", 12),
            bg="grey", fg="white", relief="flat", command=self.reset_form, cursor="hand2"
        )
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.cancel_button.pack_forget()

    def handle_add_or_update(self):
        room_id = self.room_id_var.get()
        customer_id = self.customer_id_var.get()
        check_in = self.checkin_entry.get()
        check_out = self.checkout_entry.get()
        status = self.status_entry.get()
        
        
        # Check if Customer Id Exit in the Customer Table
        if int(customer_id) not in self.customer_options:
            print(self.customer_options)
            messagebox.showerror("Error", "Customer ID not found.")
            return
       
        # Calculate the number of days between check-in and check-out
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        duration = (check_out_date - check_in_date).days  # Duration in days

        if duration <= 0:
            messagebox.showerror("Error", "Check-out date cannot be earlier than check-in date.")
            return
        # Get Room Id's Position in room_options
        room_index = -1 # Default value
        for i in range(len(self.room_options)):
            if self.room_options[i]['Id'] == int(room_id):
                room_index = i
              
                break
        
        total_amount = duration * self.room_options[room_index]['price']

        # print(total_amount)
       
        if self.is_edit_mode:
            self.controller.update_reservation(self.current_reservation_id, room_id, customer_id, check_in, check_out, status, total_amount)
            self.reset_form()
        else:
            self.controller.add_reservation(room_id, customer_id, check_in, check_out, status, total_amount)

    def reset_form(self):
        """ Resets the form to add mode and clears entries """
        self.room_id_entry.delete(0, tk.END)
        self.customer_id_entry.delete(0, tk.END)
        self.checkin_entry.delete(0, tk.END)
        self.checkout_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        # self.total_amount_entry.delete(0, tk.END)
        self.add_button.config(text="Add Reservation")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_reservation_id = None

    def create_data_view(self):
        # Reservation List Table, including "actions" in columns
        self.reservations_list = ttk.Treeview(self.data_frame, columns=("roomId", "customerId", "checkIn", "checkOut", "status", "totalAmount", "actions"), show="headings")
        self.reservations_list.heading("roomId", text="Room ID")
        self.reservations_list.heading("customerId", text="Customer ID")
        self.reservations_list.heading("checkIn", text="Check-In")
        self.reservations_list.heading("checkOut", text="Check-Out")
        self.reservations_list.heading("status", text="Status")
        self.reservations_list.heading("totalAmount", text="Total Amount")
        self.reservations_list.heading("actions", text="Actions")

        # Set column widths and center-align
        for col in ("roomId", "customerId", "checkIn", "checkOut", "status", "totalAmount"):
            self.reservations_list.column(col, anchor="center", width=100)
        self.reservations_list.column("actions", anchor="center", width=150)

        # Bind single-click event for action handling
        self.reservations_list.bind("<Button-1>", self.on_single_click)

        # Pack room list table
        self.reservations_list.pack(fill="both", expand=True, pady=10)

        # Load all data on page load
        self.update_reservations_list(self.controller.get_all_reservations())

    def update_reservations_list(self, reservations):
        for i in self.reservations_list.get_children():
            self.reservations_list.delete(i)

        for reservation in reservations:
            reservation_id = reservation['Id']
            self.reservations_list.insert("", "end", values=(reservation['roomId'], reservation['customerId'], reservation['checkIn'], reservation['checkOut'], reservation['status'], reservation['totalAmount'], "Edit | Delete"), iid=reservation_id)

    def on_single_click(self, event):
        item_id = self.reservations_list.identify_row(event.y)
        column_id = self.reservations_list.identify_column(event.x)

        if item_id and column_id == '#7':  # '#7' corresponds to the "actions" column
            reservation_data = self.reservations_list.item(item_id, "values")
            reservation_id = item_id  # Get the reservation ID directly from the row

            x_offset = event.x - self.reservations_list.bbox(item_id, column_id)[0]

            if x_offset < 75:
                self.initiate_edit_reservation(reservation_data)
            else:
                self.delete_reservation(reservation_id)  # Pass the correct reservation_id
                


    def initiate_edit_reservation(self, reservation_data):
        """Switches the form to edit mode for the selected reservation and populates form fields."""
        self.current_reservation_id = reservation_data[0]  # Store reservation ID
        self.is_edit_mode = True
        self.add_button.config(text="Update Reservation")  
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        # Populate form fields with reservation data
        self.room_id_entry.delete(0, tk.END)
        self.room_id_entry.insert(0, reservation_data[1])
        self.customer_id_entry.delete(0, tk.END)
        self.customer_id_entry.insert(0, reservation_data[2])
        self.check_in_entry.delete(0, tk.END)
        self.check_in_entry.insert(0, reservation_data[3])
        self.check_out_entry.delete(0, tk.END)
        self.check_out_entry.insert(0, reservation_data[4])
        self.status_entry.delete(0, tk.END)
        self.status_entry.insert(0, reservation_data[5])
        # self.total_amount_entry.delete(0, tk.END)
        # self.total_amount_entry.insert(0, reservation_data[6])

    def delete_reservation(self, reservation_id):
        """Prompts the user to confirm deletion of a reservation and deletes it if confirmed."""
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?")
        if response:
            self.controller.delete_reservation(reservation_id)  # Use reservation_id directly
            self.update_reservations_list(self.controller.get_all_reservations())  # Refresh the list

    def is_customer_valid(self, customer_id):
        """
        Function to check if the provided customer ID exists in the customer database.
        Replace this with your actual logic to check against your customer database.

        :param customer_id: ID of the customer to check
        :return: True if the customer exists, False otherwise
        """
        # Assuming self.customer_options contains a list of valid customer IDs (e.g., 'Customer ID - 1', 'Customer ID - 2', ...)
        if customer_id in self.customer_options:
            return True
        else:
            return False