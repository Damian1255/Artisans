import hashlib
import random
from classes import Customer, Admin
from components import DbManager
from configuration import config

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

        customer_id = random.randint(1, 999999)
        while customer_id in customer_list:
            customer_id = random.randint(1, 999999)

        customer.set_user_id(customer_id)
        customer_list[customer_id] = customer

        db.update_customer_list(customer_list)
        print(f'New customer {customer.get_username()} created!')


    def create_admin(self, username, first_name, last_name, password, email):
        password = hashlib.md5((password + salt).encode()).hexdigest()
        admin = Admin.Admin(username, first_name, last_name, password, email)

        admin_list = db.get_admin_list()

        admin_id = random.randint(1, 999999)
        while admin_id in admin_list:
            admin_id = random.randint(1, 999999)
        
        admin.set_user_id(admin_id)
        admin_list[admin_id] = admin

        db.update_admin_list(admin_list)
        print(f'New admin {admin.get_username()} created!')


    def get_customer(self, id):
        try:
            customer = db.get_customer_list()[id]
            print(f'Customer {customer.get_username()} successfully retrieved!')
            return customer
        except:
            print(f'Customer {id} not found!')
            return False
    

    def get_admin(self, id):
        admin = db.get_admin_list()[id]
        print(f'Admin {admin.get_username()} successfully retrieved!')
        return admin
    
    def get_admin_list(self):
        print(f'Admin list successfully retrieved!')
        return db.get_admin_list()

    def update_customer(self, id, first_name, last_name, email, dob):
        customer_list = db.get_customer_list()
        customer = customer_list[id]

        customer.set_first_name(first_name)
        customer.set_last_name(last_name)
        customer.set_email(email)
        customer.set_birthdate(dob)

        customer_list[id] = customer
        db.update_customer_list(customer_list)
        print(f'Customer {customer.get_username()} successfully updated!')
        return True
    
    def update_password(self, id, password):
        customer_list = db.get_customer_list()
        customer = customer_list[id]

        password = hashlib.md5((password + salt).encode()).hexdigest()
        customer.set_password(password)

        customer_list[id] = customer
        db.update_customer_list(customer_list)
        print(f'Customer {customer.get_username()} password successfully updated!')
        return True

    def get_customer_list(self):
        print(f'Customer list successfully retrieved!')
        return db.get_customer_list()
    

    def get_admin_list(self):
        print(f'Admin list successfully retrieved!')
        return db.get_admin_list()
    

    def delete_customer(self, id):
        try:
            customer_list = db.get_customer_list()
            del customer_list[id]
            db.update_customer_list(customer_list)
            print(f'Customer {id} successfully deleted!')
            return True
        except:
            return False


    def delete_admin(self, id):
        try:
            admin_list = db.get_admin_list()
            del admin_list[id]
            db.update_admin_list(admin_list)
            print(f'Admin {id} successfully deleted!')
            return True
        except:
            return False
    