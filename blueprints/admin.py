from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash
import os
from configuration import config
from werkzeug.utils import secure_filename
from components import ProductManager

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin/")
product_manager = ProductManager.ProductManager()

@admin_blueprint.route("/")
def index():
    try:
        if session['logged_in'] and session['isadmin']:
            return render_template('admin/index.html')
        else:
            return redirect(url_for('/'))
    except:
        return redirect(url_for('account.login'))
    
@admin_blueprint.route('/ecommerce')
def ecommerce():
    return render_template('admin/dashboard-eCommerce.html')
    

@admin_blueprint.route('/sign-up')
def admin_signup():
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
        tag = request.form['tag']
        image = img_urls

        product_manager.add_product(title, price, quantity, image, description, category, tag)

    return render_template('admin/product-temp.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
