from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import shelve
import User
import logging
import hashlib

app = Flask(__name__)
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
            user_list = db['Users']
            db.close()

            username = request.json['username']
            # hashes password for comparison
            password = hashlib.md5(
                (request.json['password'] + salt).encode()).hexdigest()

            for key in user_list:
                if user_list[key].get_username() == username and user_list[key].get_password() == password:
                    print(f"User {user_list[key].get_username()} logged in successfully!")

                    # creates session
                    session['user_id'] = user_list[key].get_user_id()
                    session['first_name'] = user_list[key].get_first_name()
                    session['last_name'] = user_list[key].get_last_name()
                    session['username'] = user_list[key].get_username()
                    session['logged_in'] = True

                    return jsonify({'success': True})
            return jsonify({'success': False})
        except:
            print("Error in retrieving Users from storage.db.")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # retrieves user list from storage.db
        try:
            db = shelve.open('storage.db', 'c')
        except:
            print("Error in retrieving storage.db.")
        try:
            user_list = db['Users']
        except:
            user_list = {}

        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        # hash password
        password = hashlib.md5(
            (request.json['password'] + salt).encode()).hexdigest()

        # checks if username or email is already taken
        available = True
        for key in user_list:
            if user_list[key].get_username() == username or user_list[key].get_email() == email:
                available = False
                break

        if available == False:
            return jsonify({
                'available': available,
                'success': False
            })
        else:
            user = User.User(username, first_name, last_name, password, email)
            user_list[user.get_user_id] = user
            db['Users'] = user_list
            db.close()

            print(
                f"User created successfully! Username: {user.get_username()} Password: {user.get_password()} Email: {user.get_email()}")
            return jsonify({
                'available': available,
                'success': True
            })

    return render_template('login.html', show_reg=True)


@app.route('/logout')
def logout():
    # removes session
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('username', None)
    session['logged_in'] = False

    return redirect(url_for('index'))


@app.route('/account')
def account():
    if session['logged_in'] == True:
        return render_template('my-account.html')
    else:
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template('admin/index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
