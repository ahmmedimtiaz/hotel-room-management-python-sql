from app.billing.billing_model import PaymentModel

class PaymentController:
    def __init__(self, view):
        self.model = PaymentModel()
        self.view = view

    def add_payment(self, reservation_id, amount, discount, payment_date, status):
        """Adds a new payment to the database."""
        self.model.create_payment(reservation_id, amount, discount, payment_date, status)
        self.refresh_payment_list()

    def get_all_payments(self):
        """Fetches all payments from the database."""
        return self.model.fetch_all_payments()

    def search_payments(self, keyword):
        """Searches payments by a keyword."""
        return self.model.search_payments(keyword)

    def update_payment(self, payment_id, reservation_id, amount, discount, payment_date, status):
        """Updates a specific payment based on payment_id."""
        self.model.update_payment(payment_id, reservation_id, amount, discount, payment_date, status)
        self.refresh_payment_list()

    def delete_payment(self, payment_id):
        """Deletes a specific payment by payment_id."""
        self.model.delete_payment(payment_id)
        self.refresh_payment_list()

    def refresh_payment_list(self):
        """Refreshes the view's payment list with the latest data from the model."""
        payments = self.model.fetch_all_payments()
        self.view.update_payments_list(payments)

    def get_reservation_ids(self):
        """Fetches all reservation IDs from the reservations table."""
        return self.model.fetch_reservation_ids()
