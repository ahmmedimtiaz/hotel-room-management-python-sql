# models/customer_model.py

import pymysql
from pymysql.cursors import DictCursor
from app.database import Database

class CustomerModel:
    def __init__(self):
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        # Use DictCursor to get results as dictionaries
        self.cursor = self.conn.cursor(DictCursor)

    def create_customer(self, name, email, phone, address, created_by=1):
        query = "INSERT INTO customers (name, email, phone, address, createdBy) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, email, phone, address, created_by))
        self.conn.commit()

    def fetch_all_customers(self):
        query = "SELECT * FROM customers"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_customers(self, keyword):
        query = """
        SELECT * FROM customers
        WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s OR address LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword, keyword))
        return self.cursor.fetchall()

    def update_customer(self, customer_id, name, email, phone, address):
        query = "UPDATE customers SET name = %s, email = %s, phone = %s, address = %s WHERE Id = %s"
        self.cursor.execute(query, (name, email, phone, address, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        query = "DELETE FROM customers WHERE Id = %s"
        self.cursor.execute(query, (customer_id,))
        self.conn.commit()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
