import shelve

class DbManager:
    def __init__(self,):
        self.path = 'storage/storage.db'

    def get_customer_list(self):
        try:
            db = shelve.open(self.path, 'c')
        except:
            print('Error opening database.')
        try:
            customer_list = db['Customers']
        except:
            customer_list = {}
        
        db.close()
        return customer_list
    
    def get_admin_list(self):
        try:
            db = shelve.open(self.path, 'c')
        except:
            print('Error opening database.')
        try:
            admin_list = db['Admins']
        except:
            admin_list = {}

        db.close()
        return admin_list