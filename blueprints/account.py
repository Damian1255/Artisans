from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from components import UserManager, CartManager

account_blueprint = Blueprint(name="account", import_name=__name__, url_prefix="/account/")
user_manager = UserManager.UserManager()
cart_manager = CartManager.CartManager()

@account_blueprint.route('/')
def account():
    try:
        if session['logged_in']:
            user = user_manager.get_customer(session['user_id'])

        return render_template('artisan/my-account.html', user=user)
    except:
        return redirect(url_for('account.login'))

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        # authenticates customer user
        auth = user_manager.authenticate_customer(username, password)
        if auth['success']:
            create_session(auth['user'])
            return jsonify({'success': True})
            
        return jsonify({'success': False})
    try:
        if session['logged_in']:
            return redirect(url_for('index'))
        else:
            return render_template('artisan/login.html')
    except:
        return render_template('artisan/login.html')
    
@account_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':        
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        gender = request.json['gender']
        dob = request.json['dob']
        password = request.json['password']
        
        if user_manager.username_available(username) and user_manager.email_available(email):
            user_manager.create_customer(username, first_name, last_name, password, email, dob, gender)
            
            return jsonify({ 'success': True })
        else:
            return jsonify({ 'success': False })
            
    try:
        if session['logged_in']:
            return redirect(url_for('index'))
        else:
            return render_template('artisan/login.html', show_reg=True)
    except:
        return render_template('artisan/login.html', show_reg=True)
    
@account_blueprint.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        dob = request.json['dob']
        password = request.json['password']

        if user_manager.update_customer(id, first_name, last_name, password, email, dob):
            return jsonify({'success': True})

        return jsonify({'success': False})
    return redirect(url_for('account'))
    
@account_blueprint.route('/logout')
def logout():
    # removes session
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('username', None)
    session['logged_in'] = False
    
    return redirect(url_for('index'))

@account_blueprint.route('/delete', methods=['POST', 'GET'])
def delete_user():
    customer_id = int(request.form['customer_id'])
    if user_manager.delete_customer(customer_id):
        cart_manager.delete_items_by_customer(customer_id)
        return redirect(url_for('account.logout'))

    return redirect(url_for('account.account'))
    
def create_session(user):
    session['user_id'] = user.get_user_id()
    session['first_name'] = user.get_first_name()
    session['last_name'] = user.get_last_name()
    session['username'] = user.get_username()
    session['logged_in'] = True
