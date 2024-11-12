import re
from app.database import Database

class Utils:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()  # Use a single connection from Database
        self.curr_userId = None  # Initialize the current user id to None

    def is_valid_name(self, name):
        """Check if the name is at least 4 characters."""
        return len(name) >= 4

    def is_unique_username(self, username):
        """Check if the username is unique in the database."""
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] == 0  # True if username does not exist

    def is_strong_password(self, password):
        """Check if the password is at least 8 characters long."""
        return len(password) >= 8

    def validate_email(self,email):
        """Validate email format using regex."""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    
    def validate_phone(phone):
        """Validate phone format to ensure it's 11 digits."""
        phone_regex = r'^\d{11}$'  # Adjust to your desired phone format
        return re.match(phone_regex, phone) is not None
