import random
from classes import Cart
from components import DbManager, ProductManager
from flask import url_for

db = DbManager.DbManager()
product_manager = ProductManager.ProductManager()

class CartManager():
    def add_to_cart(self, customer_id, product_id, quantity):
        cart_list = db.get_cart_list()

        # check if there is sufficient stock against cart quantity
        product = product_manager.get_product(product_id)
        cart = CartManager.get_cart(self, customer_id)
        for item in cart:
            if item[0].get_id() == product_id:
                if item[1].get_quantity() + int(quantity) > int(product.get_quantity()):
                    print(f'Insufficient stock for product {product_id}!')
                    return False

        # check if item already exists in cart
        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_customer_id() == customer_id and cart.get_product_id() == product_id:
                cart.set_quantity(cart.get_quantity() + quantity)
                db.update_cart_list(cart_list)
                print(f'Cart item {cart_id} updated!')
                return True

        # add new item to cart
        cart_id = random.randint(1, 999999)
        while cart_id in cart_list:
            cart_id = random.randint(1, 999999)
        
        cart = Cart.Cart(cart_id, customer_id, product_id, quantity)

        cart_list[cart_id] = cart
        db.update_cart_list(cart_list)
        print(f'New cart item added: {cart_id}')
        return True

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

        db.update_cart_list(cart_list)
        print(f'Cart items by customer {customer_id} successfully deleted!')

    def delete_items_by_product(self, product_id):
        cart_list = db.get_cart_list()
        delete_list = []

        for cart_id in cart_list:
            cart = cart_list[cart_id]
            if cart.get_product_id() == product_id:
                delete_list.append(cart_id)

        for cart_id in delete_list:
            del cart_list[cart_id]

        db.update_cart_list(cart_list)
        print(f'Cart items by product {product_id} successfully deleted!')

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

    def get_cart_html(self, id):
        cart = CartManager.get_cart(self, id)
        cart_display = ""
        total_display = ""
        offcanvas_cart = ""

        for item in cart:
            cart_display += f"""
            <tr>
                <td class="product-thumbnail">
                    <a href="/artworks/{item[0].get_id()}"><img class="img-responsive ml-15px"
                        src="{ url_for('static', filename='artisan/images/product-image/')}{item[0].get_image()[0]}" alt="" /></a>
                </td>
                <td class="product-name"><a href="/artworks/{item[0].get_id()}">{item[0].get_name()}</a></td>
                <td class="product-price-cart"><span class="amount">${item[0].get_price()}</span></td>
                <td class="product-quantity">
                    <div class="cart-plus-minus">
                        <div class="dec qtybutton" onclick="updateCart({item[1].get_cart_id()}, -1)">-</div>
                        <input class="cart-plus-minus-box" type="text" name="qtybutton" id="quantity-{item[1].get_cart_id()}" value="{item[1].get_quantity()}" max="{item[0].get_quantity()}"/>
                        <div class="inc qtybutton" onclick="updateCart({item[1].get_cart_id()}, 1)">+</div>
                    </div>
                </td>
                <td class="product-subtotal">${float(item[0].get_price()) * float(item[1].get_quantity())}</td>
                <td class="product-remove">
                    <a onclick="document.getElementById('itemDialog-{item[1].get_cart_id()}').showModal();"><i class="fa fa-times"></i></a>
                </td>
                <dialog id="itemDialog-{item[1].get_cart_id()}">
                    <h2>Remove<br>{item[0].get_name()}?</h2>
                    <p>Do you want to remove this item from your cart?</p>
                    <a onclick="document.getElementById('itemDialog-{item[1].get_cart_id()}').close();" aria-label="close" class="x">❌</a>
                    <button type="button" class="dialog-btn-danger" onclick="deleteItemFromCart({item[1].get_cart_id()})">
                        <i class="fa fa-arrow-left"> </i> Remove Item
                    </button>
                </dialog>
            </tr>
            """
            total_display += f"""
            <h5>{item[0].get_name()} X {item[1].get_quantity()} <span>${float(item[0].get_price()) * float(item[1].get_quantity())}</span></h5>
            <input type="hidden" id="product-{item[1].get_cart_id()}" value="{item[0].get_id()}">
            """

            offcanvas_cart += f"""
            <li>
                <a href="/artworks/{item[0].get_id()}" class="image"><img src="{ url_for('static', filename='artisan/images/product-image/') }{item[0].get_image()[0]}"
                        alt="Cart product Image"></a>
                <div class="content">
                    <a href="/artworks/{item[0].get_id()}" class="title">{item[0].get_name()} (x{item[1].get_quantity()})</a>
                    <span class="quantity-price"><span class="amount">${float(item[1].get_quantity()) * float(item[0].get_price())}</span></span>
                </div>
            </li>
            """

        grand_total = sum([float(item[0].get_price()) * float(item[1].get_quantity()) for item in cart])
        total_display += f"""
        <div class="title-wrap"></div>
        <h4 class="grand-totall-title">Grand Total <span>${grand_total}</span></h4>
        <a href="/cart/checkout">Proceed to Checkout</a>
        """

        return cart_display, total_display, offcanvas_cart, len(cart)

