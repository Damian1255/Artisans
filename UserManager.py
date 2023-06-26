import shelve
import hashlib
import Customer, Admin

salt = "wubba lubba dub dub"

class UserManager():
    def __init__(self, db):
        self.db = shelve.open(db, 'c')

        try:
            self.customer_list = self.db['Customers']
        except:
            self.customer_list = {}

        try:
            self.admin_list = self.db['Admins']
        except:
            self.admin_list = {}
    
    def authenticate_admin(self, username, password):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        for key in self.admin_list:
            if self.admin_list[key].get_username() == username and self.admin_list[key].get_password() == password:
                return {'success': True, 'user': self.admin_list[key]}
            
        return {'success': False}
    
    def authenticate_customer(self, username, password):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        for key in self.customer_list:
            if self.customer_list[key].get_username() == username and self.customer_list[key].get_password() == password:
                return {'success': True, 'user': self.customer_list[key]}
            
        return {'success': False}
    
    def check_username_availability(self, username):
        for key in self.customer_list:
            if self.customer_list[key].get_username() == username:
                return False
        return True
    
    def check_email_availability(self, email):
        for key in self.customer_list:
            if self.customer_list[key].get_email() == email:
                return False
        return True
    
    def check_admin_username_availability(self, username):
        for key in self.admin_list:
            if self.admin_list[key].get_username() == username:
                return False
        return True
    
    def check_admin_email_availability(self, email):
        for key in self.admin_list:
            if self.admin_list[key].get_email() == email:
                return False
        return True
    
    def create_customer(self, username, first_name, last_name, password, email, dob, gender):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        customer = Customer.Customer(username, first_name, last_name, password, email, dob, gender)
        
        self.customer_list[customer.get_user_id()] = customer
        self.db['Customers'] = self.customer_list

    def create_admin(self, username, first_name, last_name, password, email):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        admin = Admin.Admin(username, first_name, last_name, password, email)

        self.admin_list[admin.get_user_id()] = admin
        self.db['Admins'] = self.admin_list

    def get_customer(self, id):
        return self.customer_list[id]
    
    def get_admin(self, id):
        return self.admin_list[id]
    
    def update_customer(self, id, first_name, last_name, password, email, dob):
        customer = self.customer_list[id]

        customer.set_first_name(first_name)
        customer.set_last_name(last_name)
        customer.set_password(password)
        customer.set_email(email)
        customer.set_birthdate(dob)

        self.customer_list[id] = customer
        self.db['Customers'] = self.customer_list
        return True
    



    

