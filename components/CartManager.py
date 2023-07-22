import random
from classes import Cart
from components import DbManager, ProductManager

db = DbManager.DbManager()

class CartManager():
    def add_to_cart(self, customer_id, product_id, quantity):
        cart_list = db.get_cart_list()

        # check if item already exists in cart
        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_customer_id() == customer_id and cart.get_product_id() == product_id:
                cart.set_quantity(cart.get_quantity() + quantity)
                db.update_cart_list(cart_list)
                print(f'Cart item {cart_id} updated!')
                return

        # add new item to cart
        cart_id = random.randint(1, 999999)
        while cart_id in cart_list:
            cart_id = random.randint(1, 999999)
        
        cart = Cart.Cart(cart_id, customer_id, product_id, quantity)

        cart_list[cart_id] = cart
        db.update_cart_list(cart_list)
        print(f'New cart added: {cart_id}')

    def delete_item(self, cart_id):
        try:
            cart_list = db.get_cart_list()
            del cart_list[cart_id]
            db.update_cart_list(cart_list)
            print(f'Cart item {cart_id} successfully deleted!')
        except:
            print(f'Cart item {cart_id} does not exist!')

    def delete_items_by_customer(self, customer_id):
        cart_list = db.get_cart_list()
        delete_list = []

        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_customer_id() == customer_id:
                delete_list.append(cart_id)

        for cart_id in delete_list:
            del cart_list[cart_id]
            print(f'Cart item {cart_id} successfully deleted!')

        db.update_cart_list(cart_list)

    def delete_items_by_product(self, product_id):
        cart_list = db.get_cart_list()
        delete_list = []

        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_product_id() == product_id:
                delete_list.append(cart_id)

        for cart_id in delete_list:
            del cart_list[cart_id]
            print(f'Cart item {cart_id} successfully deleted!')

        db.update_cart_list(cart_list)

    def get_cart(self, customer_id):
        cart_list = db.get_cart_list()
        cart_items = []

        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_customer_id() == customer_id:
                # get product
                product = ProductManager.ProductManager().get_product(cart.get_product_id())
                cart_items.append([product, cart])

        print(f'Cart items for customer {customer_id} retrieved! {len(cart_items)} items found.')
        return cart_items

    def update_cart(self, cart_id, quantity):
        try:
            cart_list = db.get_cart_list()
            cart = cart_list[cart_id]
            cart.set_quantity(quantity)
            db.update_cart_list(cart_list)
            print(f'Cart item {cart_id} successfully updated!')
        except:
            print(f'Cart item {cart_id} does not exist!')

