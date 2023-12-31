from flask import Blueprint, render_template, jsonify, request
from components import DbManager, UserManager, ProductManager, CartManager, OrderManager
from werkzeug.utils import secure_filename
from configuration import config
import os

product_bp = Blueprint(name="product_bp", import_name=__name__, url_prefix="/artworks/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()
cart_manager = CartManager.CartManager()
order_manager = OrderManager.OrderManager()


@product_bp.route('/')
def index():
    products = product_manager.get_product_list()

    prefix = 'search/?category='
    categories = {}
    categories['All'] = [len(products), '']

    for key in products:
        if products[key].get_category() not in categories:
            categories[products[key].get_category()] = [1, prefix + products[key].get_category()]
        else:
            categories[products[key].get_category()][0] += 1

    return render_template('artisan/shop-left-sidebar.html', products=products, categories=categories, count=len(products), title='Artworks')


@product_bp.route('/<int:id>')
def product_page(id):
    if product_manager.get_product(id):
        product = product_manager.get_product(id)
        customer = user_manager.get_customer(int(product.get_customer_id()))
        
        if customer:
            artist = customer.get_username()
        elif product.get_customer_id() == 00000:
            artist = "Artisan's"
        else:
            artist = 'Unknown'

        return render_template('artisan/single-product-tabstyle-2.html', product=product, artist=artist)
    else:
        return render_template('artisan/404.html'), 404


@product_bp.route('/search/' , methods=['GET', 'POST'] , endpoint='search')
def product_search():
    try:
        query = request.args.get('query')
        category = request.args.get('category')
        results = product_manager.search_product(query, category)
        
        # Get categories
        categories = {}
        if query:
            prefix = f'search/?query={query}&category='
            all_products = product_manager.search_product(query, None)
            categories['All'] = [len(all_products), f'search/?query={query}']

            if category:
                title = f'Search results for "{query}" in {category}'
            else:
                title = f'Search results for "{query}"'
        elif category:
            prefix = f'search/?category='
            all_products = product_manager.get_product_list()
            categories['All'] = [len(all_products), f'']
            title = f'{category}'

        for key in all_products:
            if all_products[key].get_category() not in categories:
                categories[all_products[key].get_category()] = [1, prefix + all_products[key].get_category()]
            else:
                categories[all_products[key].get_category()][0] += 1


        return render_template('artisan/shop-left-sidebar.html', products=results, categories=categories, count=len(all_products), title=title)
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

@product_bp.route('/delete/', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_id = request.json['product_id']

        if product_manager.delete_product(product_id):
            cart_manager.delete_items_by_product(product_id)
            order_manager.delete_orders_by_product(product_id)
        
            return jsonify({'success': True})

        return jsonify({'success': False})
    
@product_bp.route('/update/', methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        product_id = request.json['product_id']
        title = request.json['product_title']
        price = request.json['product_price']
        quantity = request.json['product_quantity']
        description = request.json['product_description']
        category = request.json['product_category']

        if product_manager.update_product(product_id, title, price, quantity, description, category):
            return jsonify({'success': True})

        return jsonify({'success': False})
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

