import shelve

class DbManager:
    def __init__(self, db):
        try:
            self.db = shelve.open(db, 'r')
        except:
            print('Error opening database.')
        try:
            self.customer_list = self.db['Customers']
        except:
            self.customer_list = {}
        try:
            self.admin_list = self.db['Admins']
        except:
            self.admin_list = {}

    def get_customer_list(self):
        return self.customer_list
    
    def get_admin_list(self):
        return self.admin_list