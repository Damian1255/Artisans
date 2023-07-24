from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash
import os
from configuration import config
from werkzeug.utils import secure_filename
from components import ProductManager, UserManager

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin/")
product_manager = ProductManager.ProductManager()
user_manager = UserManager.UserManager()

@admin_blueprint.route("/")
def index():
    try:
        if session['admin_logged_in']:
            return render_template('admin/index.html')
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('admin.login'))
    
@admin_blueprint.route('/ecommerce')
def ecommerce():
    return render_template('admin/dashboard-eCommerce.html')


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
        

@admin_blueprint.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        # save images to static/uploads
        img_urls = []
        for image in request.files.getlist('images'):
            if image and allowed_file(image.filename):
                imagename = secure_filename(image.filename)
                image.save(os.path.join(config.UPLOAD_FOLDER, imagename))
                img_urls.append(imagename)
            
            # todo: add error handling for invalid file types

        title = request.form['title']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        category = request.form['category']
        image = img_urls

        product_manager.add_product(12345, title, price, quantity, image, description, category)

    return render_template('admin/product-temp.html')

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