from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from components import DbManager, UserManager, ProductManager, CartManager, OrderManager

cart_bp = Blueprint(name="cart_bp", import_name=__name__, url_prefix="/cart/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()
order_manager = OrderManager.OrderManager()


@cart_bp.route('/', methods=['GET', 'POST'])
def cart_page():
    if 'user_id' not in session:
        return redirect(url_for('account.login'))
    
    if request.method == 'POST':
        cart_display = session['cart']

        return jsonify({'success': True,
                        'cart_display': cart_display[0],
                        'total_display': cart_display[1],
                        'offcanvas_cart': cart_display[2],
                        'cart_count': cart_display[3]
                        })
    else:
        cart = cart_manager.get_cart(session['user_id'])
        if len(cart) == 0:
            return render_template('artisan/empty-cart.html')
        
        return render_template('artisan/cart.html')


@cart_bp.route('/add/', methods=['GET', 'POST'])
def add_item():
    if 'user_id' in session and request.method == 'POST':
        product_id = int(request.json['product_id'])
        quantity = int(request.json['quantity'])

        if cart_manager.add_to_cart(session['user_id'], product_id, quantity):
            # Update cart session
            session['cart'] = cart_manager.get_cart_html(session['user_id'])
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'insuf_stock': True})

    return jsonify({'success': False, 'login_required': True})


@cart_bp.route('/delete/item/', methods=['GET', 'POST'])
def delete_item():
    if 'user_id' in session:
        product_id = int(request.json['product_id'])
        cart_manager.delete_item(product_id)

        # Update cart session
        session['cart'] = cart_manager.get_cart_html(session['user_id'])

        return jsonify({'success': True})

    return jsonify({'success': False})


@cart_bp.route('/clear/', methods=['GET', 'POST'])
def clear_cart():
    if 'user_id' in session:
        cart_manager.delete_items_by_customer(session['user_id'])

        # Update cart session
        session['cart'] = cart_manager.get_cart_html(session['user_id'])

        return jsonify({'success': True})

    return jsonify({'success': False})


@cart_bp.route('/update/', methods=['GET', 'POST'])
def update_cart():
    if 'user_id' in session:
        cart_id = int(request.json['cart_id'])
        quantity = int(request.json['quantity'])
        cart_manager.update_cart(cart_id, quantity)

        # Update cart session
        session['cart'] = cart_manager.get_cart_html(session['user_id'])

        return jsonify({'success': True})

    return jsonify({'success': False})


@cart_bp.route('/checkout/', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Add order to database
        cart = cart_manager.get_cart(session['user_id'])
        for item in cart:
            product = item[0]
            quantity = item[1].get_quantity()
            order_total = product.get_price() * quantity
            order_manager.new_order(
                session['user_id'], product.get_id(), quantity, order_total)

        # Update Product quantity
        for item in cart:
            product = item[0]
            quantity = item[1].get_quantity()
            product_manager.update_product_quantity(product.get_id(), int(product.get_quantity()) - int(quantity))

        # Clear cart
        cart_manager.delete_items_by_customer(session['user_id'])

        # Update cart session
        session['cart'] = cart_manager.get_cart_html(session['user_id'])

        return render_template('artisan/thank-you-page.html')
    else:
        if 'user_id' not in session:
            return redirect(url_for('account.login'))
        
        cart = cart_manager.get_cart(session['user_id'])
        if len(cart) == 0:
            return redirect(url_for('index'))
        
        customer = user_manager.get_customer(session['user_id'])
        grand_total = sum([float(item[0].get_price()) * float(item[1].get_quantity()) for item in cart])
        
        return render_template('artisan/checkout.html', customer=customer, cart=cart, grand_total=grand_total)
