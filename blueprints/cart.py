from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from components import DbManager, UserManager, ProductManager, CartManager

cart_bp = Blueprint(name="cart_bp", import_name=__name__, url_prefix="/cart/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()

@cart_bp.route('/')
def cart_page():
    if 'user_id' not in session:
        return redirect(url_for('account.login'))
    
    cart = cart_manager.get_cart(session['user_id'])
    grand_total = sum([item[0].get_price() * item[1].get_quantity() for item in cart])

    if len(cart) == 0:
        return render_template('artisan/empty-cart.html', cart=cart, grand_total=grand_total, empty=True)
    
    return render_template('artisan/cart.html', cart=cart, grand_total=grand_total)

@cart_bp.route('/add/', methods=['GET', 'POST'])
def add_item():
    if 'user_id' in session and request.method == 'POST':
        product_id = int(request.json['product_id'])
        quantity = int(request.json['quantity'])

        if product_manager.get_product(product_id):
            cart_manager.add_to_cart(session['user_id'], product_id, quantity)
            return jsonify({'success': True})
        
    return jsonify({'success': False})

@cart_bp.route('/delete/item/', methods=['GET', 'POST'])
def delete_item():
    if 'user_id' in session:
        product_id = int(request.json['product_id'])
        cart_manager.delete_item(product_id)

        return jsonify({'success': True})

    return jsonify({'success': False})

@cart_bp.route('/clear/', methods=['GET', 'POST'])
def clear_cart():
    if 'user_id' in session:
        cart_manager.delete_items_by_customer(session['user_id'])

        return jsonify({'success': True})

    return jsonify({'success': False})

@cart_bp.route('/update/', methods=['GET', 'POST'])
def update_cart():
    if 'user_id' in session:
        cart_id = int(request.json['cart_id'])
        quantity = int(request.json['quantity'])
        cart_manager.update_cart(cart_id, quantity)

        return jsonify({'success': True})
    
    return jsonify({'success': False})