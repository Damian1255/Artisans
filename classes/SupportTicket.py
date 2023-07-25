class SupportTicket:
    def __init__(self, id, firstName, lastName, email, countryCode, phoneNumber, subject, message):
        self.__id = id
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__countryCode = countryCode
        self.__phoneNumber = phoneNumber
        self.__subject = subject
        self.__message = message

    def get_ticket_id(self):
        return self.__id
    
    def get_first_name(self):
        return self.__firstName
    
    def get_last_name(self):
        return self.__lastName
    
    def get_email(self):
        return self.__email
    
    def get_country_code(self):
        return self.__countryCode
    
    def get_phone_number(self):
        return self.__phoneNumber
    
    def get_subject(self):
        return self.__subject
    
    def get_message(self):
        return self.__message
    
    def set_ticket_id(self, id):
        self.__id = id

    def set_first_name(self, firstName):
        self.__firstName = firstName

    def set_last_name(self, lastName):
        self.__lastName = lastName

    def set_email(self, email):
        self.__email = email

    def set_country_code(self, countryCode):
        self.__countryCode = countryCode

    def set_phone_number(self, phoneNumber):
        self.__phoneNumber = phoneNumber

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

        