import shelve
from configuration import config

class DbManager:
    def __init__(self):
        self.db_file = config.DB_PATH
        self.db = None

    def open(self):
        self.db = shelve.open(self.db_file)

    def close(self):
        self.db.close()

    def get_customer_list(self):
        self.open()
        customer_list = self.db['Customers']
        self.close()
        return customer_list
    
    def get_admin_list(self):
        self.open()
        admin_list = self.db['Admins']
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
    