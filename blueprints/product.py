from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from components import DbManager, UserManager, ProductManager, CartManager
from werkzeug.utils import secure_filename
from configuration import config
import os

product_bp = Blueprint(name="product_bp", import_name=__name__, url_prefix="/artworks/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()


@product_bp.route('/')
def index():
    return render_template('artisan/shop-left-sidebar.html', products=product_manager.get_product_list())


@product_bp.route('/<int:id>')
def product_page(id):
    if product_manager.get_product(id):
        return render_template('artisan/single-product-tabstyle-2.html', product=product_manager.get_product(id))
    else:
        return render_template('artisan/404.html'), 404


@product_bp.route('/search/' , methods=['GET', 'POST'] , endpoint='search')
def product_search():
    try:
        query = request.args.get('query')
        results = product_manager.search_product(query)

        return render_template('artisan/shop-left-sidebar.html', products=results)
    except:
        return render_template('artisan/404.html'), 404

@product_bp.route('/new/', methods=['GET', 'POST'])
def new_artwork():
    if request.method == 'POST':
        # save images to static/uploads
        img_urls = []
        for image in request.files.getlist('product_images'):
            if image and allowed_file(image.filename):
                imagename = secure_filename(image.filename)
                image.save(os.path.join(config.UPLOAD_FOLDER, imagename))
                img_urls.append(imagename)
            else:
                return jsonify({'success': False, 'message': 'Invalid file type'})

        customer_id = request.form['customer_id']
        title = request.form['product_title']
        price = request.form['product_price']
        quantity = request.form['product_quantity']
        description = request.form['product_description']
        category = request.form['product_category']
        image = img_urls

        result = product_manager.add_product(customer_id, title, price, quantity, image, description, category)
        if result['success']:
            return jsonify({'success': True, 'product_id': result['product_id']})

    return jsonify({'success': False})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

