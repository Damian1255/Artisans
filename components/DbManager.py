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

    def get_customer_list(self):
        return self.customer_list