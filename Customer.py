import User

class Customer(User.User):
    def __init__(self, username, first_name, last_name, password, email, birthdate, gender):
        super().__init__(username, first_name, last_name, password, email)
        self.__address = ''
        self.__gender = gender
        self.__birthdate = birthdate
        self.__user_type = "Customer"

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_gender(self):
        return self.__gender
    
    def set_gender(self, gender):
        self.__gender = gender

    def get_birthdate(self):
        return self.__birthdate
    
    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def get_user_type(self):
        return self.__user_type
    
    def set_user_type(self, user_type):
        self.__user_type = user_type