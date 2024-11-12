import pymysql
from pymysql.cursors import DictCursor
from app.database import Database

class PaymentModel:
    def __init__(self):
        # Establish the database connection
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        # Use DictCursor to get results as dictionaries
        self.cursor = self.conn.cursor(DictCursor)

    def create_payment(self, reservation_id, amount, discount, payment_date, status):
        """Inserts a new payment record into the payments table."""
        query = """
        INSERT INTO payments (reservationId, amount, discount, paymentDate, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (reservation_id, amount, discount, payment_date, status))
        self.conn.commit()

    def fetch_all_payments(self):
        """Fetches all payments from the payments table."""
        query = "SELECT * FROM payments"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_payment_by_id(self, payment_id):
        """Fetches a payment by its ID."""
        query = "SELECT * FROM payments WHERE Id = %s"
        self.cursor.execute(query, (payment_id,))
        return self.cursor.fetchone()

    def fetch_reservation_ids(self):
        """Fetches reservation IDs as a list of dictionaries with 'Id' keys."""
        query = "SELECT Id FROM reservations"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_payment(self, payment_id, reservation_id, amount, discount, payment_date, status):
        """Updates an existing payment record based on payment ID."""
        query = """
        UPDATE payments
        SET reservationId = %s, amount = %s, discount = %s, paymentDate = %s, status = %s
        WHERE Id = %s
        """
        self.cursor.execute(query, (reservation_id, amount, discount, payment_date, status, payment_id))
        self.conn.commit()

    def delete_payment(self, payment_id):
        """Deletes a payment record by its ID."""
        query = "DELETE FROM payments WHERE Id = %s"
        self.cursor.execute(query, (payment_id,))
        self.conn.commit()

    def search_payments(self, keyword):
        """Searches payments by matching keyword with reservation ID, amount, or status."""
        query = """
        SELECT * FROM payments
        WHERE reservationId LIKE %s OR amount LIKE %s OR status LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword))
        return self.cursor.fetchall()

    def __del__(self):
        """Closes cursor and connection upon object deletion."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
