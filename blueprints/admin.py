from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash
import os
from configuration import config
from werkzeug.utils import secure_filename

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
def admin_signup():
    return render_template('admin/temp-sign-up.html')


@admin_blueprint.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        images = request.json['images']
        print(images.files)

        # check if the post request has the file part
        if 'images' not in request.files:
            print('No images part')
            return redirect(request.url)
        
        file = request.files['images']

        if file.filename == '':
            print('No selected images')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))

    return render_template('admin/product-temp.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
