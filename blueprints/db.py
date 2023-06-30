from flask import Blueprint, render_template, session, redirect, url_for
from components import DbManager

db_blueprint = Blueprint(name="db", import_name=__name__, url_prefix="/db/")
db_manager = DbManager.DbManager('storage/storage.db')

@db_blueprint.route('/')
def db():
    customer_list = db_manager.get_customer_list()
    admin_list = db_manager.get_admin_list()

    return render_template('dbmanager/db.html', customers=customer_list, admins=admin_list)
