from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from components import DbManager, UserManager, ProductManager

product_bp = Blueprint(name="product_bp", import_name=__name__, url_prefix="/product/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
product_manager = ProductManager.ProductManager()

@product_bp.route('/<int:id>')
def product_page(id):
    if product_manager.get_product(id):
        return render_template('artisan/single-product-tabstyle-2.html', product=product_manager.get_product(id))
    else:
        return render_template('artisan/404.html'), 404


