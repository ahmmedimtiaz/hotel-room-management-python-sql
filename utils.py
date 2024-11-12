import re

class Utils:
    @staticmethod
    def validate_email(email):
        """Validate email format using regex."""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Validate phone format to ensure it's 11 digits."""
        phone_regex = r'^\d{11}$'  # Adjust to your desired phone format
        return re.match(phone_regex, phone) is not None
