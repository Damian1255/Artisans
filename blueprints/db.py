from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from components import DbManager, UserManager, ProductManager, CartManager, SupportManager, OrderManager

db_blueprint = Blueprint(name="db", import_name=__name__, url_prefix="/db/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()
support_manager = SupportManager.SupportManager()
order_manager = OrderManager.OrderManager()

@db_blueprint.route('/')
def index():
    customer_list = db.get_customer_list()
    admin_list = db.get_admin_list()
    product_list = db.get_product_list()
    cart_list = db.get_cart_list()
    support_list = db.get_support_ticket_list()
    order_list = db.get_order_list()

    return render_template('db/db.html', customers=customer_list, admins=admin_list,
                           products=product_list, cart_items=cart_list, support_tickets=support_list, orders=order_list)

@db_blueprint.route('/delete/admin/<int:id>', methods=['GET', 'POST'])
def delete_admin(id):
    user_manager.delete_admin(id)
    return jsonify({'success': True})

@db_blueprint.route('/delete/customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    user_manager.delete_customer(id)
    cart_manager.delete_items_by_customer(id)
    order_manager.delete_orders_by_customer(id)

    return jsonify({'success': True})

@db_blueprint.route('/delete/product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product_manager.delete_product(id)
    cart_manager.delete_items_by_product(id)
    order_manager.delete_orders_by_product(id)
    
    return jsonify({'success': True})

@db_blueprint.route('/delete/cart/<int:id>', methods=['GET', 'POST'])
def delete_cart(id):
    cart_manager.delete_item(id)
    return jsonify({'success': True})

@db_blueprint.route('/delete/ticket/<int:id>', methods=['GET', 'POST'])
def delete_ticket(id):
    support_manager.delete_ticket(id)
    return jsonify({'success': True})

@db_blueprint.route('/delete/order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    order_manager.delete_order(id)
    return jsonify({'success': True})
