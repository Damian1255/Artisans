from flask import Flask, render_template, request, redirect, url_for, session
import shelve
import User
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
app.secret_key = 'nani'

#disables logging
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

            username = request.form['username']
            password = request.form['password']

            for key in user_list:
                if user_list[key].get_username() == username and user_list[key].get_password() == password:
                    print(f"User {user_list[key].get_username()} has logged in successfully!")

                    #creates session
                    session['first_name'] = user_list[key].get_first_name()
                    session['last_name'] = user_list[key].get_last_name()
                    session['username'] = user_list[key].get_username()
                    session['logged_in'] = True

                    return redirect(url_for('index'))
        except:
            print("Error in retrieving Users from storage.db.")  
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db = shelve.open('storage.db', 'c')
        except:
            print("Error in retrieving storage.db.")
        try:
            user_list = db['Users']
        except:
            user_list = {}

        first_name = request.form['first-name']
        last_name = request.form['last-name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.User(username, first_name, last_name, password, email)

        user_list[user.get_user_id] = user
        db['Users'] = user_list
        db.close()

        print(f"User created successfully! {user.get_username()} {user.get_password()} {user.get_email()}")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
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

if __name__ == '__main__':
    app.run(debug=True)