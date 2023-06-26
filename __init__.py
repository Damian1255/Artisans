from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import User, Customer, Admin, UserManager
import logging

app = Flask(__name__, static_url_path='/static')
log = logging.getLogger('werkzeug')

app.secret_key = 'nani'
salt = "wubba lubba dub dub"

# disables flask logging
log.disabled = True
app.logger.disabled = True

user_manager = UserManager.UserManager('storage.db')

@app.route('/')
def index():
    # creates session if it doesn't exist
    if 'logged_in' not in session:
        session['logged_in'] = False
    
    return render_template('index.html')

@app.route('/2')
def index2():
    return render_template('index-2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        # authenticates admin user
        auth = user_manager.authenticate_admin(username, password)
        if auth['success']:
            create_session(auth['user'], True)
            return jsonify({'success': True})

        # authenticates customer user
        auth = user_manager.authenticate_customer(username, password)
        if auth['success']:
            create_session(auth['user'], False)
            return jsonify({'success': True})
            
        return jsonify({'success': False})
    
    elif session['logged_in'] == False:
        return render_template('login.html')
    else:
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':        
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        gender = request.json['gender']
        dob = request.json['dob']
        password = request.json['password']
        
        # registers user
        if request.json['isadmin']:
            if user_manager.admin_email_available(username) and user_manager.admin_email_available(email):
                user_manager.create_admin(username, first_name, last_name, password, email)
                return jsonify({ 'success': True })
            else:
                return jsonify({ 'success': False })
        else:
            if user_manager.username_available(username) and user_manager.email_available(email):
                user_manager.create_customer(username, first_name, last_name, password, email, dob, gender)
                return jsonify({ 'success': True })
            else:
                return jsonify({ 'success': False })

    elif session['logged_in'] == False:
        return render_template('login.html', show_reg=True)
    else:
        return redirect(url_for('index'))
    
@app.route('/update-user/<int:id>', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    # removes session
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('username', None)
    session.pop('isadmin', None)
    session['logged_in'] = False

    return redirect(url_for('index'))


@app.route('/account')
def account():
    if session['logged_in']:
        if session['isadmin']:
            user = user_manager.get_admin(session['user_id'])
        else:
            user = user_manager.get_customer(session['user_id'])

        return render_template('my-account.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/admin/')
def dashboard():
    if session['logged_in'] == True and session['isadmin'] == True:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/sign-up')
def admin_signin():
    return render_template('admin/temp-sign-up.html')

def create_session(user, isadmin):
    session['user_id'] = user.get_user_id()
    session['first_name'] = user.get_first_name()
    session['last_name'] = user.get_last_name()
    session['username'] = user.get_username()
    session['logged_in'] = True
    session['isadmin'] = isadmin


if __name__ == '__main__':
    app.run(debug=True)
