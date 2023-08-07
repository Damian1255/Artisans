from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from components import UserManager, CartManager, OrderManager, ProductManager
from configuration import config

account_blueprint = Blueprint(
    name="account", import_name=__name__, url_prefix="/account/")
user_manager = UserManager.UserManager()
cart_manager = CartManager.CartManager()
order_manager = OrderManager.OrderManager()
product_manager = ProductManager.ProductManager()


@account_blueprint.route('/')
def account():
    if 'logged_in' in session:
        user = user_manager.get_customer(session['user_id'])
        orders = order_manager.get_orders_by_customer(session['user_id'])
        order_list = []

        for order in orders:
            product = product_manager.get_product(order.get_product_id())
            order_list.append([order, product])

        artworks = product_manager.get_products_by_customer((session['user_id']))
        user_artworks = []
        for artwork in artworks:
            sold = order_manager.get_ordered_quantity_by_product(artwork.get_id())
            user_artworks.append([artwork, sold])


        total_sold = 0
        total_profit = 0.0
        
        artworks = order_manager.get_orders_by_seller((session['user_id']))
        for artwork in artworks:
            total_profit += round(artwork.get_order_total() - artwork.get_order_total() * artwork.get_comm_rate())
            total_sold += artwork.get_order_quantity()
            
            
        return render_template('artisan/my-account.html', user=user,
                               orders=order_list, user_artworks=user_artworks,
                               total_sold=total_sold, total_profit=total_profit,
                               comm_rate=config.COMM_RATE)

    return redirect(url_for('account.login'))


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        # authenticates customer user
        auth = user_manager.authenticate_customer(username, password)
        if auth['success']:
            create_session(auth['user'])
            return jsonify({'success': True})

        return jsonify({'success': False})
    try:
        if session['logged_in']:
            return redirect(url_for('index'))
        else:
            return render_template('artisan/login.html')
    except:
        return render_template('artisan/login.html')


@account_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        gender = request.json['gender']
        dob = request.json['dob']
        password = request.json['password']

        if user_manager.username_available(username) and user_manager.email_available(email):
            user_manager.create_customer(
                username, first_name, last_name, password, email, dob, gender)

            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

    try:
        if session['logged_in']:
            return redirect(url_for('index'))
        else:
            return render_template('artisan/login.html', show_reg=True)
    except:
        return render_template('artisan/login.html', show_reg=True)


@account_blueprint.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        dob = request.json['dob']

        if user_manager.update_customer(id, first_name, last_name, email, dob):
            return jsonify({'success': True})

        return jsonify({'success': False})
    return redirect(url_for('account'))


@account_blueprint.route('/password/update', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        user_id = int(request.json['user_id'])
        current_password = request.json['current_password']
        new_password = request.json['new_password']

        # authenticates customer user
        auth = user_manager.authenticate_customer(
            session['username'], current_password)
        if auth['success']:
            if user_manager.update_password(user_id, new_password):
                return jsonify({'success': True})

        return jsonify({'success': False})

    return redirect(url_for('account'))


@account_blueprint.route('/logout')
def logout():
    # removes session
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('username', None)
    session.pop('cart', None)
    session['logged_in'] = False

    return redirect(url_for('index'))


@account_blueprint.route('/delete', methods=['POST', 'GET'])
def delete_user():
    customer_id = int(request.form['customer_id'])
    if user_manager.delete_customer(customer_id):

        cart_manager.delete_items_by_customer(customer_id)
        order_manager.delete_orders_by_customer(customer_id)
        product_manager.delete_products_by_customer(customer_id)

        return redirect(url_for('account.logout'))

    return redirect(url_for('account.account'))


def create_session(user):
    session['user_id'] = user.get_user_id()
    session['first_name'] = user.get_first_name()
    session['last_name'] = user.get_last_name()
    session['username'] = user.get_username()
    session['cart'] = cart_manager.get_cart_html(session['user_id'])
    session['logged_in'] = True
