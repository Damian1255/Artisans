import shelve
from configuration import config

class DbManager:
    def __init__(self):
        self.db_file = config.DB_PATH
        self.db = None

    def open(self):
        try:
            self.db = shelve.open(self.db_file)
        except IOError:
            print('Error opening database.')
            exit(1)
            
    def close(self):
        self.db.close()

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
    
    def update_customer_list(self, customer_list):
        self.open()
        self.db['Customers'] = customer_list
        self.close()

    def update_admin_list(self, admin_list):
        self.open()
        self.db['Admins'] = admin_list
        self.close()
    