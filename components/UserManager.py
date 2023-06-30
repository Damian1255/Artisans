import shelve
import hashlib
from classes import Customer, Admin
from components import DbManager
from config import config

salt = config.HASH_SALT
db = DbManager.DbManager()

class UserManager():
    def authenticate_admin(self, username, password):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        admin_list = db.get_admin_list()

        for key in db.get_admin_list():
            if admin_list[key].get_username() == username and admin_list[key].get_password() == password:
                print(f'Admin {admin_list[key].get_username()} authenticated!')
                return {'success': True, 'user': admin_list[key]}
            
        return {'success': False}
    

    def authenticate_customer(self, username, password):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        customer_list = db.get_customer_list()

        for key in customer_list:
            if customer_list[key].get_username() == username and customer_list[key].get_password() == password:
                print(f'Customer {customer_list[key].get_username()} authenticated!')
                return {'success': True, 'user': customer_list[key]}
            
        return {'success': False}
    

    def username_available(self, username):
        customer_list = db.get_customer_list()

        for key in customer_list:
            if customer_list[key].get_username() == username:
                return False
            
        return True
    

    def email_available(self, email):
        customer_list = db.get_customer_list()

        for key in customer_list:
            if customer_list[key].get_email() == email:
                return False
            
        return True
    

    def admin_username_available(self, username):
        admin_list = db.get_admin_list()

        for key in admin_list:
            if admin_list[key].get_username() == username:
                return False
            
        return True
    

    def admin_email_available(self, email):
        admin_list = db.get_admin_list()

        for key in admin_list:
            if admin_list[key].get_email() == email:
                return False
            
        return True
    

    def create_customer(self, username, first_name, last_name, password, email, dob, gender):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        customer = Customer.Customer(username, first_name, last_name, password, email, dob, gender)
        
        customer_list = db.get_customer_list()
        customer_list[customer.get_user_id()] = customer
        db.update_customer_list(customer_list)

        print(f'New customer {customer.get_username()} created!')


    def create_admin(self, username, first_name, last_name, password, email):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        admin = Admin.Admin(username, first_name, last_name, password, email)

        admin_list = db.get_admin_list()
        admin_list[admin.get_user_id()] = admin
        db.update_admin_list(admin_list)

        print(f'New admin {admin.get_username()} created!')


    def get_customer(self, id):
        return db.get_customer_list()[id]
    

    def get_admin(self, id):
        return db.get_admin_list()[id]
    

    def update_customer(self, id, first_name, last_name, password, email, dob):
        customer_list = db.get_customer_list()
        customer = customer_list[id]

        customer.set_first_name(first_name)
        customer.set_last_name(last_name)
        customer.set_password(password)
        customer.set_email(email)
        customer.set_birthdate(dob)

        customer_list[id] = customer
        db.update_customer_list(customer_list)
        print(f'Customer {customer.get_username()} successfully updated!')

        return True
    

    def get_customer_list(self):
        print(f'Customer list successfully retrieved!')
        return db.get_customer_list()
    

    def get_admin_list(self):
        print(f'Admin list successfully retrieved!')
        return db.get_admin_list()
    