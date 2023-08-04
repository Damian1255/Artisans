import random, datetime
from classes import Order
from components import DbManager, ProductManager
from configuration import config

db = DbManager.DbManager()
comm_rate = config.COMM_RATE

class OrderManager():
    def new_order(self, customer_id, product_id, seller_id, order_quantity, order_total):
        order_list = db.get_order_list()

        order_id = random.randint(100000, 999999)
        while order_id in order_list:
            order_id = random.randint(100000, 999999)

        order_date = datetime.datetime.now().strftime("%Y-%m-%d")
        order = Order.Order(order_id, customer_id, product_id, seller_id, order_quantity, order_total, order_date, comm_rate)
        order_list[order_id] = order

        db.update_order_list(order_list)
        print(f"Order {order_id} created")
        return True
    
    def get_order(self, order_id):
        order_list = db.get_order_list()
        if order_id in order_list:
            return order_list[order_id]
        else:
            return False
        
    def get_order_list(self):
        return db.get_order_list()
    
    def get_orders_by_customer(self, customer_id):
        order_list = db.get_order_list()
        customer_orders = []

        for order in order_list:
            if order_list[order].get_customer_id() == customer_id:
                customer_orders.append(order_list[order])
        return customer_orders
    
    def get_orders_by_product(self, product_id):
        order_list = db.get_order_list()
        product_orders = []

        for order in order_list:
            if order_list[order].get_product_id() == product_id:
                product_orders.append(order_list[order])
        return product_orders
    
    def get_orders_by_seller(self, seller_id):
        order_list = db.get_order_list()
        seller_orders = []

        for order in order_list:
            if int(order_list[order].get_seller_id()) == seller_id:
                seller_orders.append(order_list[order])
        return seller_orders

    def get_orders_by_date(self, order_date):
        order_list = db.get_order_list()
        date_orders = []

        for order in order_list:
            if order_list[order].get_order_date() == order_date:
                date_orders.append(order_list[order])
        return date_orders
    
    def delete_order(self, order_id):
        order_list = db.get_order_list()
        if order_id in order_list:
            del order_list[order_id]
            db.update_order_list(order_list)
            print(f"Order {order_id} deleted")
            return True
        else:
            return False
    
    def delete_orders_by_customer(self, customer_id):
        order_list = db.get_order_list()
        delete_list = []

        for order_id in order_list:
            order = order_list[order_id]
            if order.get_customer_id() == customer_id:
                delete_list.append(order_id)

        for order_id in delete_list:
            del order_list[order_id]

        db.update_order_list(order_list)
        print(f'Orders by customer {customer_id} successfully deleted!')
    
    def delete_orders_by_product(self, product_id):
        order_list = db.get_order_list()
        delete_list = []

        for order_id in order_list:
            order = order_list[order_id]
            if order.get_product_id() == product_id:
                delete_list.append(order_id)

        for order_id in delete_list:
            del order_list[order_id]

        db.update_order_list(order_list)
        print(f'Orders by product {product_id} successfully deleted!')
    
    def get_ordered_quantity_by_product(self, product_id):
        order_list = db.get_order_list()
        total_quantity = 0

        for order_id in order_list:
            order = order_list[order_id]
            if order.get_product_id() == product_id:
                total_quantity += order.get_order_quantity()
        
        return total_quantity
    
