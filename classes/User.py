class User:
    count_id = 0
    def __init__(self, username, first_name, last_name, password, email):
        self.__class__.count_id += 1
        self.__user_id = self.__class__.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__password = password
        self.__email = email

    def get_user_id(self):
        return self.__user_id
    
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_username(self):
        return self.__username
    
    def set_username(self, username):
        self.__username = username

    def get_first_name(self):
        return self.__first_name
    
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__last_name
    
    def set_last_name(self, last_name):
        self.__last_name = last_name
    
    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email
