# models/reservation_model.py

import pymysql
from pymysql.cursors import DictCursor
from app.database import Database

class ReservationModel:
    def __init__(self):
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        # Use DictCursor to get results as dictionaries
        self.cursor = self.conn.cursor(DictCursor)

    def create_reservation(self, room_id, customer_id, check_in, check_out, status, total_amount):
        """Inserts a new reservation into the reservations table."""
        query = """
        INSERT INTO reservations (roomId, customerId, checkIn, checkOut, status, totalAmount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (room_id, customer_id, check_in, check_out, status, total_amount))
        self.conn.commit()

    def fetch_all_reservations(self):
        """Fetches all reservations from the reservations table."""
        query = "SELECT * FROM reservations"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_reservations(self, keyword):
        """Searches reservations by matching keyword with room ID, customer ID, or status."""
        query = """
        SELECT * FROM reservations
        WHERE roomId LIKE %s OR customerId LIKE %s OR status LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword))
        return self.cursor.fetchall()

    def update_reservation(self, reservation_id, room_id, customer_id, check_in, check_out, status, total_amount):
        """Updates a reservation's details based on reservation ID."""
        query = """
        UPDATE reservations
        SET roomId = %s, customerId = %s, checkIn = %s, checkOut = %s, status = %s, totalAmount = %s
        WHERE Id = %s
        """
        self.cursor.execute(query, (room_id, customer_id, check_in, check_out, status, total_amount, reservation_id))
        self.conn.commit()

    def delete_reservation(self, reservation_id):
        """Deletes a reservation by its ID."""
        query = "DELETE FROM reservations WHERE Id = %s"
        self.cursor.execute(query, (reservation_id,))
        self.conn.commit()

    def __del__(self):
        """Closes cursor and connection upon object deletion."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
