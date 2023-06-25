from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import shelve
import User, Customer, Admin
import logging
import hashlib

app = Flask(__name__, static_url_path='/static')
log = logging.getLogger('werkzeug')

app.secret_key = 'nani'
salt = "wubba lubba dub dub"

# disables flask logging
log.disabled = True
app.logger.disabled = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def index2():
    return render_template('index-2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            db = shelve.open('storage.db', 'r')
        except Exception:
            print("Something went wrong.")
        try:
            customer_list = db['Customers']
        except:
            customer_list = {}
        try:
            admin_list = db['Admins']
        except:
            admin_list = {}

        db.close()

        username = request.json['username']
        # hashes password for comparison
        password = hashlib.md5((request.json['password'] + salt).encode()).hexdigest()

        # logs in admin if username and password matches
        for key in admin_list:
            if admin_list[key].get_username() == username and admin_list[key].get_password() == password:
                print(f"Admin {admin_list[key].get_username()} logged in successfully!")
                create_session(admin_list[key], True)

                return jsonify({'success': True})

        # logs in user if username and password matches
        for key in customer_list:
            if customer_list[key].get_username() == username and customer_list[key].get_password() == password:
                print(f"User {customer_list[key].get_username()} logged in successfully!")
                create_session(customer_list[key], False)

                return jsonify({'success': True})
            
        return jsonify({'success': False})
    elif session['logged_in'] == False:
        return render_template('login.html')
    else:
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # retrieves user list from storage.db
        try:
            db = shelve.open('storage.db', 'c')
        except:
            print("Error in retrieving storage.db.")
        try:
            customer_list = db['Customers']
        except:
            customer_list = {}
        try:
            admin_list = db['Admins']
        except:
            admin_list = {}
        
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        gender = request.json['gender']
        dob = request.json['dob']
        # hash password
        password = hashlib.md5((request.json['password'] + salt).encode()).hexdigest()

        # checks if username or email is already taken by a user
        available = True
        for key in customer_list:
            if customer_list[key].get_username() == username or customer_list[key].get_email() == email:
                available = False
                break
        # checks if username or email is already taken by a admin
        for key in admin_list:
            if admin_list[key].get_username() == username or admin_list[key].get_email() == email:
                available = False
                break

        if available == False:
            return jsonify({
                'available': available,
            })
        
        if request.json['isadmin']:
            admin = Admin.Admin(username, first_name, last_name, password, email)
            admin_list[admin.get_user_id()] = admin
            db['Admins'] = admin_list
            print(f"Admin {admin.get_username()} created successfully!")
        else:
            customer = Customer.Customer(username, first_name, last_name, password, email, dob, gender)
            customer_list[customer.get_user_id()] = customer
            db['Customers'] = customer_list
            print(f"Customer {customer.get_username()} created successfully!")

        db.close()
        return jsonify({
            'available': available,
        })
    elif session['logged_in'] == False:
        return render_template('login.html', show_reg=True)
    else:
        return redirect(url_for('index'))
    
@app.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        try:
            db = shelve.open('storage.db', 'c')
            customer_list = db['Customers']
            
            # retrieves user object from user list
            customer = customer_list[id]

            # updates user object
            customer.set_first_name(request.json['first_name'])
            customer.set_last_name(request.json['last_name'])
            customer.set_email(request.json['email'])
            customer.set_password(hashlib.md5((request.json['password'] + salt).encode()).hexdigest())
            customer.set_birthdate(request.json['dob'])

            # updates user object in user list
            customer_list[id] = customer
            db['Customers'] = customer_list
            db.close()

            print(f"User {customer.get_username()} updated successfully!")
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            print("Something went wrong.")
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
    if session['logged_in'] == True:
        # retrieves user list from storage.db
        try:
            db = shelve.open('storage.db', 'r')
            customer_list = db['Customers']
            admin_list = db['Admins']
            db.close()
                
            # retrieves user object from user list
            if session['isadmin'] == True:
                user = admin_list[session['user_id']]
            else:
                user = customer_list[session['user_id']]

            print(f"{user.get_username()} information retrieved successfully!")
            return render_template('my-account.html', user=user)
        except Exception as e:
            print(e)
            print("An error occurred.")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/')
def dashboard():
    if session['logged_in'] == True and session['isadmin'] == True:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin-sign-up')
def admin_signin():
    return render_template('admin/temp-sign-up.html')

def get_user_list():
    try:
        db = shelve.open('storage.db', 'c')
    except:
        print("Error in retrieving storage.db.")
    try:
        user_list = db['Users']
    except:
        user_list = {}
    return user_list

def create_session(user, isadmin):
    session['user_id'] = user.get_user_id()
    session['first_name'] = user.get_first_name()
    session['last_name'] = user.get_last_name()
    session['username'] = user.get_username()
    session['logged_in'] = True
    session['isadmin'] = isadmin


if __name__ == '__main__':
    app.run(debug=True)
