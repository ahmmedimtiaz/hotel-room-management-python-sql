# controllers/reservation_controller.py

from app.reservation.reservation_model import ReservationModel

class ReservationController:
    def __init__(self, view):
        self.model = ReservationModel()
        self.view = view

    def add_reservation(self, room_id, customer_id, check_in, check_out, status, total_amount):
        """Adds a new reservation to the database."""
        self.model.create_reservation(room_id, customer_id, check_in, check_out, status, total_amount)
        self.refresh_reservation_list()

    def get_all_reservations(self):
        """Fetches all reservations from the database."""
        return self.model.fetch_all_reservations()

    def search_reservations(self, keyword):
        """Searches reservations by a keyword."""
        return self.model.search_reservations(keyword)

    def update_reservation(self, reservation_id, room_id, customer_id, check_in, check_out, status, total_amount):
        """Updates a specific reservation based on reservation_id."""
        self.model.update_reservation(reservation_id, room_id, customer_id, check_in, check_out, status, total_amount)
        self.refresh_reservation_list()

    def delete_reservation(self, reservation_id):
        """Deletes a specific reservation by reservation_id."""
        self.model.delete_reservation(reservation_id)
        self.refresh_reservation_list()

    def refresh_reservation_list(self):
        """Refreshes the view's reservation list with the latest data from the model."""
        reservations = self.model.fetch_all_reservations()
        self.view.update_reservation_list(reservations)
