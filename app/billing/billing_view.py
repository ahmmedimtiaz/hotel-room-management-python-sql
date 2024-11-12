import tkinter as tk
from tkinter import ttk, messagebox
from app.billing.billing_controller import PaymentController
from app.billing.billing_model import PaymentModel
from datetime import datetime
from tkcalendar import DateEntry 


class BillingView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False
        self.current_payment_id = None  # Track payment being edited

        # Initialize the controller with a reference to self
        self.controller = PaymentController(self)

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)

        # Fetch all reservation IDs for dropdown
        payment_model = PaymentModel()
        self.reservation_options = payment_model.fetch_reservation_ids()

        self.reservation_ids = [payment['Id'] for payment in self.reservation_options]

        # Title
        tk.Label(
            self.frame, text="Payment Management Section", bg=secondary_color,
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Payment Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Payment List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)

        # Initialize data view but do not load data yet
        self.create_data_view()

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Payment", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Reservation ID (Dropdown)
        tk.Label(self.form_frame, text="Reservation ID:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.reservation_id_var = tk.StringVar()
        self.reservation_id_var.set(self.reservation_ids[0] if self.reservation_ids else "No reservations available")  # Set default value
        self.reservation_id_entry = tk.OptionMenu(self.form_frame, self.reservation_id_var, *self.reservation_ids)
        self.reservation_id_entry.config(font=("Helvetica", 14))
        self.reservation_id_entry.pack(fill="x", pady=10, ipady=5)

        # Payment Date
        tk.Label(self.form_frame, text="Payment Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.payment_date_entry = DateEntry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid", date_pattern="yyyy-mm-dd")
        self.payment_date_entry.pack(fill="x", pady=5, ipady=5)

        # Payment Amount
        tk.Label(self.form_frame, text="Payment Amount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.amount_entry.pack(fill="x", pady=5, ipady=5)
        
        # Discount
        tk.Label(self.form_frame, text="Discount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.discount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.discount_entry.pack(fill="x", pady=5, ipady=5)

        # Status
        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.status_entry.pack(fill="x", pady=5, ipady=5)

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Payment", font=("Helvetica", 14, "bold"),
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
        reservation_id = self.reservation_id_var.get()
        payment_date = self.payment_date_entry.get()
        amount = self.amount_entry.get()
        status = self.status_entry.get()
        discount = self.discount_entry.get()

        # Validate payment amount
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")
            return

        if self.is_edit_mode:
            self.controller.update_payment(self.current_payment_id,reservation_id, amount,discount,payment_date, status)
            self.reset_form()
        else:
            self.controller.add_payment(reservation_id,amount,discount,payment_date, status)

    def reset_form(self):
        """ Resets the form to add mode and clears entries """
        self.reservation_id_var.set("Select Reservation")
        self.amount_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.add_button.config(text="Add Payment")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_payment_id = None

    def create_data_view(self):
        # Payment List Table, including "actions" in columns
        self.payments_list = ttk.Treeview(self.data_frame, columns=("id","reservationId", "paymentDate", "amount","discount", "status", "actions"), show="headings")
        self.payments_list.heading("id", text="Reservation ID")
        self.payments_list.heading("reservationId", text="Reservation ID")
        self.payments_list.heading("paymentDate", text="Payment Date")
        self.payments_list.heading("amount", text="Amount")
        self.payments_list.heading("discount", text="Discount")
        self.payments_list.heading("status", text="Status")
        self.payments_list.heading("actions", text="Actions")

        # Set column widths and center-align
        for col in ("id","reservationId", "paymentDate", "amount","discount", "status"):
            self.payments_list.column(col, anchor="center", width=80)
        self.payments_list.column("actions", anchor="center", width=150)

        # Bind single-click event for action handling
        self.payments_list.bind("<Button-1>", self.on_single_click)

        # Pack payment list table
        self.payments_list.pack(fill="both", expand=True, pady=10)

        # Load all data on page load
        self.update_payments_list(self.controller.get_all_payments())

    def update_payments_list(self, payments):
        for i in self.payments_list.get_children():
            self.payments_list.delete(i)

        for payment in payments:
            payment_id = payment['Id']
            self.payments_list.insert("", "end", values=(payment['Id'],payment['reservationId'], payment['paymentDate'], payment['amount'],payment['discount'], payment['status'], "Edit | Delete"), iid=payment_id)

    def on_single_click(self, event):
        item_id = self.payments_list.identify_row(event.y)
        column_id = self.payments_list.identify_column(event.x)

        if item_id and column_id == '#7':  # '#5' corresponds to the "actions" column
            payment_data = self.payments_list.item(item_id, "values")
            payment_id = item_id  # Get the payment ID directly from the row

            x_offset = event.x - self.payments_list.bbox(item_id, column_id)[0]

            if x_offset < 75:
                self.initiate_edit_payment(payment_data)
            else:
                self.delete_payment(payment_id)  # Pass the correct payment_id

    def initiate_edit_payment(self, payment_data):
        """Switches the form to edit mode for the selected payment and populates form fields."""
        self.current_payment_id = payment_data[0]  # Store payment ID
        self.is_edit_mode = True
        self.add_button.config(text="Update Payment")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        # Populate form fields with payment data
        # self.reservation_id_entry.delete(0, tk.END)
        self.reservation_id_var.set("Select Reservation")
        self.reservation_id_var.set(payment_data[1])
        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, payment_data[2])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, payment_data[3])
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, payment_data[4])
        self.status_entry.delete(0, tk.END)
        self.status_entry.insert(0, payment_data[5])

    def delete_payment(self, payment_id):
        """Prompts the user to confirm deletion of a payment and deletes it if confirmed."""
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payment?")
        if response:
            self.controller.delete_payment(payment_id)  # Use payment_id directly
            self.update_payments_list(self.controller.get_all_payments())  # Refresh the list
