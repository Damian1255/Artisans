from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from components import DbManager, UserManager, ProductManager, CartManager

product_bp = Blueprint(name="product_bp", import_name=__name__, url_prefix="/artworks/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()


@product_bp.route('/')
def index():
    if 'user_id' in session:
        cart = cart_manager.get_cart(session['user_id'])
    else:
        cart = []
    return render_template('artisan/shop-left-sidebar.html', products=product_manager.get_product_list(), cart=cart)


@product_bp.route('/<int:id>')
def product_page(id):
    if product_manager.get_product(id):
        if 'user_id' in session:
            cart = cart_manager.get_cart(session['user_id'])
        else:
            cart = []
        return render_template('artisan/single-product-tabstyle-2.html', product=product_manager.get_product(id), cart=cart)
    else:
        return render_template('artisan/404.html'), 404


@product_bp.route('/search/' , methods=['GET', 'POST'] , endpoint='search')
def product_search():
    try:
        query = request.args.get('query')
        results = product_manager.search_product(query)

        if 'user_id' in session:
            cart = cart_manager.get_cart(session['user_id'])
        else:
            cart = []

        return render_template('artisan/shop-left-sidebar.html', products=results, cart=cart)
    except:
        return render_template('artisan/404.html'), 404

