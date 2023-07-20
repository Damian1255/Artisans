import random
from classes import Cart
from components import DbManager, ProductManager

db = DbManager.DbManager()

class CartManager():
    def add_to_cart(self, customer_id, product_id, quantity):
        cart_list = db.get_cart_list()

        cart_id = random.randint(1, 999999)
        while cart_id in cart_list:
            cart_id = random.randint(1, 999999)
        
        cart = Cart.Cart(cart_id, customer_id, product_id, quantity)

        cart_list[cart_id] = cart
        db.update_cart_list(cart_list)
        print(f'New cart added: {cart_id}')

    def delete_item(self, id):
        cart_list = db.get_cart_list()
        del cart_list[id]
        db.update_cart_list(cart_list)
        print(f'Cart item {id} successfully deleted!')

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


