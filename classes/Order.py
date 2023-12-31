class Order:
    def __init__(self, order_id, customer_id, product_id, seller_id, order_quantity, order_total, order_date, comm_rate):
        self.__order_id = order_id
        self.__customer_id = customer_id
        self.__product_id = product_id
        self.__seller_id = seller_id
        self.__order_quantity = order_quantity
        self.__order_date = order_date
        self.__order_total = order_total
        self.__comm_rate = comm_rate

    def get_order_id(self):
        return self.__order_id

    def get_customer_id(self):
        return self.__customer_id
    
    def get_seller_id(self):
        return self.__seller_id
    
    def get_product_id(self):
        return self.__product_id
    
    def get_order_quantity(self):
        return self.__order_quantity

    def get_order_date(self):
        return self.__order_date

    def get_order_total(self):
        return self.__order_total
    
    def get_comm_rate(self):
        return self.__comm_rate
    
    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_seller_id(self, seller_id):
        self.__seller_id = seller_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_order_date(self, order_date):
        self.__order_date = order_date

    def set_order_total(self, order_total):
        self.__order_total = order_total

    def set_order_quantity(self, order_quantity):
        self.__order_quantity = order_quantity

    def set_comm_rate(self, comm_rate):
        self.__comm_rate = comm_rate
    