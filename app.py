from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from components import ProductManager
import logging

from blueprints.admin import admin_blueprint
from blueprints.account import account_blueprint
from blueprints.db import db_blueprint
from blueprints.product import product_bp
from blueprints.cart import cart_bp

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('configuration/config.py')
app.register_blueprint(admin_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(db_blueprint)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)

# disables flask logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

product_manager = ProductManager.ProductManager()

@app.route('/')
def index():
    return render_template('artisan/index.html', products=product_manager.get_product_list())

@app.route('/about')
def about():
    return render_template('artisan/about.html')

@app.route('/customer-support')
def customer_support():
    return render_template('artisan/customer-support.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('artisan/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
