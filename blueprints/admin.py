from flask import Blueprint, render_template, session, redirect, url_for

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin/")

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
def admin_signin():
    return render_template('admin/temp-sign-up.html')
