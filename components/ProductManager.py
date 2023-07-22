import random
from classes import Product
from components import DbManager

db = DbManager.DbManager()

class ProductManager():
    def add_product(self, name, price, quantity, image, description, category):
        product_list = db.get_product_list()

        product_id = random.randint(1, 999999)
        while product_id in product_list:
            product_id = random.randint(1, 999999)
        
        product = Product.Product(product_id, name, float(price), int(quantity), image, description, category)

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

    def get_product_list_by_category(self, category):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_category() == category]

    def get_product_list_by_tag(self, tag):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_tag() == tag]

    def get_product_list_by_category_and_tag(self, category, tag):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_category() == category and product_list[key].get_tag() == tag]

    def get_product_list_by_search(self, search):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if search.lower() in product_list[key].get_name().lower()]

    def get_product_list_by_category_and_search(self, category, search):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_category() == category and search.lower() in product_list[key].get_name().lower()]

    def get_product_list_by_tag_and_search(self, tag, search):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_tag() == tag and search.lower() in product_list[key].get_name().lower()]

    def get_product_list_by_category_and_tag_and_search(self, category, tag, search):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_category() == category and product_list[key].get_tag() == tag and search.lower() in product_list[key].get_name().lower()]

    def get_product_list_by_price_range(self, min, max):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_price() >= min and product_list[key].get_price() <= max]

    def get_product_list_by_category_and_price_range(self, category, min, max):
        product_list = db.get_product_list()
        return [product_list[key] for key in product_list if product_list[key].get_category() == category and product_list[key].get_price() >= min and product_list[key].get_price() <= max]
    
