class Product:
    def __init__(self, id, title, price, quantity, image, description, category):
        self.__id = id
        self.__title = title
        self.__price = price
        self.__quantity = quantity
        self.__image = image
        self.__description = description
        self.__category = category
        self.__rating = 0
        self.__reviews = []

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__title
    
    def get_price(self):
        return self.__price
    
    def get_quantity(self):
        return self.__quantity
    
    def get_image(self):
        return self.__image
    
    def get_description(self):
        return self.__description
    
    def get_category(self):
        return self.__category
    
    def get_rating(self):
        return self.__rating
    
    def get_reviews(self):
        return self.__reviews
    
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__title = name

    def set_price(self, price):
        self.__price = price

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_image(self, image):
        self.__image = image

    def set_description(self, description):
        self.__description = description

    def set_category(self, category):
        self.__category = category

    def set_rating(self, rating):
        self.__rating = rating

    def set_reviews(self, reviews):
        self.__reviews = reviews
        
