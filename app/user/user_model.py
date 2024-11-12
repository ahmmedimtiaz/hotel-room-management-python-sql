import bcrypt
from app.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()  # Use a single connection from Database
        self.curr_userId = None  # Initialize the current user id to None

    def register_user(self, name, username, email, password):
        """Registers a new user with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (name, email, username, hashed_password))
                self.conn.commit()
        except Exception as e:
            print(f"Error in register_user: {e}")
        finally:
            self.conn.close()

    def authenticate_user(self, username, password):
        """Authenticates a user by username and password."""
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT Id, password FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                # Convert the stored password to bytes before comparison
                if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                    self.curr_userId = result[0]
                    return True
        except Exception as e:
            print(f"Error in authenticate_user: {e}")
        return False
