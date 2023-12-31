import random, datetime
from classes import Order
from components import DbManager, ProductManager
from configuration import config

# Order Manager is used to create, delete, and get orders from the database

db = DbManager.DbManager()
comm_rate = config.COMM_RATE

class OrderManager():
    # Creates a new order and adds it to the database
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
    
    # Returns an order object from the database
    def get_order(self, order_id):
        order_list = db.get_order_list()
        if order_id in order_list:
            return order_list[order_id]
        else:
            return False
    
    # Returns a list of all orders in the database
    def get_order_list(self):
        return db.get_order_list()
    
    # Returns a the orders by a specific customer
    def get_orders_by_customer(self, customer_id):
        order_list = db.get_order_list()
        customer_orders = []

        for order in order_list:
            if order_list[order].get_customer_id() == customer_id:
                customer_orders.append(order_list[order])
        return customer_orders
    
    # Returns a the orders by a specific product
    def get_orders_by_product(self, product_id):
        order_list = db.get_order_list()
        product_orders = []

        for order in order_list:
            if order_list[order].get_product_id() == product_id:
                product_orders.append(order_list[order])
        return product_orders
    
    # Returns a the orders by a specific seller
    def get_orders_by_seller(self, seller_id):
        order_list = db.get_order_list()
        seller_orders = []

        for order in order_list:
            if int(order_list[order].get_seller_id()) == seller_id:
                seller_orders.append(order_list[order])
        return seller_orders

    # Deletes an order from the database
    def delete_order(self, order_id):
        order_list = db.get_order_list()
        if order_id in order_list:
            del order_list[order_id]
            db.update_order_list(order_list)
            print(f"Order {order_id} deleted")
            return True
        else:
            return False
    
    # Deletes orders made by a specific customer
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
    
    # Deletes orders from a specific product
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
    
    # get total quantity of a product ordered
    def get_ordered_quantity_by_product(self, product_id):
        order_list = db.get_order_list()
        total_quantity = 0

        for order_id in order_list:
            order = order_list[order_id]
            if order.get_product_id() == product_id:
                total_quantity += order.get_order_quantity()
        
        return total_quantity
    
    # get list of top sellers
    def get_top_sellers(self):
        product_manager = ProductManager.ProductManager()
        product_list = product_manager.get_product_list()
        top_sellers = []
        
        for product_id in product_list:
            product = product_list[product_id]
            total_quantity = self.get_ordered_quantity_by_product(product_id)
            top_sellers.append([product, total_quantity])
        
        top_sellers.sort(key=lambda x: x[1], reverse=True)
        return top_sellers[:5]
    
    # get list of top customers
    def get_top_customers(self):
        customer_list = []
        customers = db.get_customer_list()
        for customer_id in customers:
            total_sales = 0

            orders = OrderManager.get_orders_by_customer(self, customer_id)
            for order in orders:
                total_sales += order.get_order_total()
            customer_list.append([customers[customer_id], total_sales, len(orders)])
        
        customer_list.sort(key=lambda x: x[1], reverse=True)
        return customer_list
