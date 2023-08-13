import shelve
from configuration import config

# DbManager class is used to manage the input and output of data to and from the database.

class DbManager:
    # Initialize the database file
    def __init__(self):
        self.db_file = config.DB_PATH
        self.db = None

    # Open the database file
    def open(self):
        try:
            self.db = shelve.open(self.db_file)
        except IOError:
            print('Error opening database.')
            exit(1)
    
    # Close the database file
    def close(self):
        self.db.close()

    # Get the customer list from the database
    def get_customer_list(self):
        self.open()
        try:
            customer_list = self.db['Customers']
        except KeyError:
            customer_list = {}
            print('No customers found in database.')
            self.db['Customers'] = customer_list

        self.close()
        return customer_list
    
    # Get the admin list from the database
    def get_admin_list(self):
        self.open()
        try:
            admin_list = self.db['Admins']
        except KeyError:
            admin_list = {}
            print('No admins found in database.')
            self.db['Admins'] = admin_list

        self.close()
        return admin_list

    # Get the product list from the database
    def get_product_list(self):
        self.open()
        try:
            product_list = self.db['Products']
        except KeyError:
            product_list = {}
            print('No products found in database.')
            self.db['Products'] = product_list

        self.close()
        return product_list
    
    # Get the cart list from the database
    def get_cart_list(self):
        self.open()
        try:
            cart_list = self.db['Cart']
        except KeyError:
            cart_list = {}
            print('No cart found in database.')
            self.db['Cart'] = cart_list

        self.close()
        return cart_list
    
    # Get the order list from the database
    def get_order_list(self):
        self.open()
        try:
            order_list = self.db['Orders']
        except KeyError:
            order_list = {}
            print('No orders found in database.')
            self.db['Orders'] = order_list

        self.close()
        return order_list
    
    # Get the support ticket list from the database
    def get_support_ticket_list(self):
        self.open()
        try:
            support_list = self.db['Support_Tickets']
        except KeyError:
            support_list = {}
            print('No Support Tickets found in database.')
            self.db['Support_Tickets'] = support_list

        self.close()
        return support_list
    
    # Update the customer list in the database
    def update_customer_list(self, customer_list):
        self.open()
        self.db['Customers'] = customer_list
        self.close()

    # Update the admin list in the database
    def update_admin_list(self, admin_list):
        self.open()
        self.db['Admins'] = admin_list
        self.close()

    # Update the product list in the database
    def update_product_list(self, product_list):
        self.open()
        self.db['Products'] = product_list
        self.close()

    # Update the cart list in the database
    def update_cart_list(self, cart_list):
        self.open()
        self.db['Cart'] = cart_list
        self.close()

    # Update the order list in the database
    def update_order_list(self, order_list):
        self.open()
        self.db['Orders'] = order_list
        self.close()

    # Update the support ticket list in the database
    def update_support_ticket_list(self, support_list):
        self.open()
        self.db['Support_Tickets'] = support_list
        self.close()
    