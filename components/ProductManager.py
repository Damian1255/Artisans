import random
from classes import Product
from components import DbManager

db = DbManager.DbManager()

class ProductManager():
    def add_product(self, customer_id, name, price, quantity, image, description, category):
        product_list = db.get_product_list()

        product_id = random.randint(1, 999999)
        while product_id in product_list:
            product_id = random.randint(1, 999999)
        
        product = Product.Product(product_id, customer_id, name, float(price), int(quantity), image, description, category)
        product_list[product_id] = product
        
        db.update_product_list(product_list)
        print(f'New product added: {name}')

    def delete_product(self, id):
        product_list = db.get_product_list()
        del product_list[id]
        db.update_product_list(product_list)
        print(f'Product {id} successfully deleted!')

    def get_product_list(self):
        return db.get_product_list()

    def get_product(self, id):
        product_list = db.get_product_list()
        try:
            return product_list[id]
        except:
            print(f'Product {id} does not exist!')
            return False
        
    def update_product_quantity(self, product_id, quantity):
        product_list = db.get_product_list()
        try:
            product_list[product_id].set_quantity(quantity)
            db.update_product_list(product_list)
            print(f'Product {product_id} successfully updated!')
        except:
            print(f'Product {product_id} does not exist!')

        
    def search_product(self, query):
        product_list = db.get_product_list()
        results = {}
        for product in product_list.values():
            if query.lower() in product.get_name().lower():
                results[product.get_id()] = product
        return results
    