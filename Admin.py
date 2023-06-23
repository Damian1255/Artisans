import User

class Admin(User.User):
    def __init__(self, username, first_name, last_name, password, email):
        super().__init__(username, first_name, last_name, password, email)
        self.__user_type = "Admin"
    
    def get_user_type(self):
        return self.__user_type
    
    def set_user_type(self, user_type):
        self.__user_type = user_type