# controllers/customer_controller.py

from app.customer.customers_model import CustomerModel

class CustomerController:
    def __init__(self, view):
        self.model = CustomerModel()
        self.view = view

    def add_customer(self, name, email, phone, address):
        self.model.create_customer(name, email, phone, address)
        self.refresh_customer_list()

    def get_all_customers(self):
        return self.model.fetch_all_customers()

    def search_customers(self, keyword):
        return self.model.search_customers(keyword)

    def update_customer(self, customer_id, name, email, phone, address):
        self.model.update_customer(customer_id, name, email, phone, address)
        self.refresh_customer_list()

    def delete_customer(self, customer_id):
        self.model.delete_customer(customer_id)
        self.refresh_customer_list()

    def refresh_customer_list(self):
        customers = self.model.fetch_all_customers()
        self.view.update_customer_list(customers)
