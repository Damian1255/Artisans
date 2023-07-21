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
    
    return render_template('artisan/cart.html', cart=cart_manager.get_cart(session['user_id']))

@cart_bp.route('/add/', methods=['GET', 'POST'])
def add_item():
    if 'user_id' in session and request.method == 'POST':
        product_id = int(request.json['product_id'])
        quantity = int(request.json['quantity'])

        if product_manager.get_product(product_id):
            cart_manager.add_to_cart(session['user_id'], product_id, quantity)
            return jsonify({'success': True})
        
    return jsonify({'success': False})
