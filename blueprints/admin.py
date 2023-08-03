from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash
import os, pandas as pd
from datetime import datetime
from configuration import config
from werkzeug.utils import secure_filename
from components import ProductManager, UserManager, OrderManager

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin/")
product_manager = ProductManager.ProductManager()
user_manager = UserManager.UserManager()
order_manager = OrderManager.OrderManager()


@admin_blueprint.route("/")
def index():
    try:
        if session['admin_logged_in']:
            return render_template('admin/dashboard-eCommerce.html')
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('admin.login'))
    

@admin_blueprint.route("/support")
def support():
    try:
        if session['admin_logged_in']:
            return render_template('admin/dashboard-human-resources.html')
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('admin.login'))
    

@admin_blueprint.route("/products")
def products():
    if session['admin_logged_in']:
        products = product_manager.get_product_list()
        product_list = []
        
        for key in products:
            sold = order_manager.get_ordered_quantity_by_product(products[key].get_id())
            product_list.append([products[key], sold])

        return render_template('admin/ecommerce-products.html', products=product_list)

    return redirect(url_for('admin.login'))
    

@admin_blueprint.route("/products/<int:product_id>")
def product(product_id):
    if session['admin_logged_in']:
        product = product_manager.get_product(product_id)
        if product:
            return render_template('admin/ecommerce-products-details.html', product=product)
        
        return redirect(url_for('admin.products'))
    
    return redirect(url_for('admin.login'))


@admin_blueprint.route('/products/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        # save images to static/uploads
        img_urls = []
        for image in request.files.getlist('product_images'):
            if image and allowed_file(image.filename):
                imagename = secure_filename(image.filename)
                image.save(os.path.join(config.UPLOAD_FOLDER, imagename))
                img_urls.append(imagename)

        title = request.form['title']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        category = request.form['category']
        image = img_urls

        product_manager.add_product(00000, title, price, quantity, image, description, category)
        return redirect(url_for('admin.products'))

    if session['admin_logged_in']:
        return render_template('admin/ecommerce-add-new-products.html')
    
    return redirect(url_for('admin.login'))


@admin_blueprint.route("/products/orders")
def orders():
    if session['admin_logged_in']:
        orders = order_manager.get_order_list()
        order_list = []
        for order in orders:
            customer = user_manager.get_customer(orders[order].get_customer_id())
            product = product_manager.get_product(orders[order].get_product_id())
            order_list.append([orders[order], customer, product])

        return render_template('admin/ecommerce-orders.html', orders=order_list)

    return redirect(url_for('admin.login'))
    

@admin_blueprint.route('/products/orders/delete', methods=['GET', 'POST'])
def delete_order():
    order_id = request.json['order_id']
    order_manager.delete_order(order_id)

    return jsonify({'success': True})


@admin_blueprint.route("/staffs")
def staffs():
    try:
        if session['admin_logged_in']:
            admin_list = user_manager.get_admin_list()

            return render_template('admin/app-contact-list.html', staffs=admin_list)
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('admin.login'))
    

@admin_blueprint.route("/staffs/new")
def new_staff():
    try:
        if session['admin_logged_in']:
            return render_template('admin/app-contact-new.html')
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('admin.login'))
    
@admin_blueprint.route('/staffs/delete', methods=['GET', 'POST'])
def delete_admin():
    admin_id = request.json['admin_id']
    user_manager.delete_admin(admin_id)

    return jsonify({'success': True})


@admin_blueprint.route("/profile")
def profile():
    if session['admin_logged_in']:
        admin = user_manager.get_admin(session['admin_id'])
        return render_template('admin/user-profile.html', admin=admin)

    return redirect(url_for('admin.login'))


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        # authenticates customer user
        auth = user_manager.authenticate_admin(username, password)
        if auth['success']:
            create_session(auth['user'])
            return jsonify({'success': True})
            
        return jsonify({'success': False})
    
    return render_template('admin/authentication-signin.html')


@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':        
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if user_manager.admin_username_available(username) and user_manager.admin_email_available(email):
            user_manager.create_admin(username, first_name, last_name, password, email)

            return jsonify({ 'success': True })
        else:
            return jsonify({ 'success': False })
    
    return render_template('admin/temp-sign-up.html')


@admin_blueprint.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        records = []

        orders = order_manager.get_order_list()
        for order in orders:
            c = user_manager.get_customer(orders[order].get_customer_id())
            p = product_manager.get_product(orders[order].get_product_id())

            date = orders[order].get_order_date()
            customer = c.get_first_name() + ' ' + c.get_last_name()
            product = p.get_name()
            quantity = int(orders[order].get_order_quantity())
            sales = float(orders[order].get_order_total())

            records.append({
                'date': date,
                'customer': customer,
                'product': product,
                'quantity': quantity,
                'sales': sales
            })

        # check for empty gap in date to fill with 0
        start_date = datetime.strptime(records[0]['date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d').date()

        for date in pd.date_range(start_date, end_date):
            date = date.strftime('%Y-%m-%d')
            if not any(record['date'] == date for record in records):
                records.append({
                    'date': date, 'customer': '', 'product': '', 'quantity': 0, 'sales': 0
                })

        df = pd.DataFrame(records).groupby(['date']).sum(numeric_only=True).reset_index()
        result_bydate = df.to_dict('list')

        return jsonify({
            'result_bydate': result_bydate
        })


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@admin_blueprint.route('/logout')
def logout():
    # removes session
    session['admin_id'] = None
    session['admin_first_name'] = None
    session['admin_last_name'] = None
    session['admin_username'] = None
    session['admin_logged_in'] = False
    
    return redirect(url_for('admin.login'))


def create_session(user):
    session['admin_id'] = user.get_user_id()
    session['admin_first_name'] = user.get_first_name()
    session['admin_last_name'] = user.get_last_name()
    session['admin_username'] = user.get_username()
    session['admin_logged_in'] = True