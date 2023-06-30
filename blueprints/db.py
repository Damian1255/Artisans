from flask import Blueprint, render_template, session, redirect, url_for
from components import DbManager

db_blueprint = Blueprint(name="db", import_name=__name__, url_prefix="/db/")

db = DbManager.DbManager()

@db_blueprint.route('/')
def index():
    customer_list = db.get_customer_list()
    admin_list = db.get_admin_list()

    return render_template('dbmanager/db.html', customers=customer_list, admins=admin_list)
