from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from components import DbManager, UserManager

db_blueprint = Blueprint(name="db", import_name=__name__, url_prefix="/db/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()

@db_blueprint.route('/')
def index():
    customer_list = db.get_customer_list()
    admin_list = db.get_admin_list()

    return render_template('db/db.html', customers=customer_list, admins=admin_list)


@db_blueprint.route('/delete/admin/<int:id>', methods=['GET', 'POST'])
def delete_admin(id):
    user_manager.delete_admin(id)
    return jsonify({'success': True})


@db_blueprint.route('/delete/customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    user_manager.delete_customer(id)
    return jsonify({'success': True})