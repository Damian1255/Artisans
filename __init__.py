from flask import Flask, render_template, request, redirect, url_for
import shelve
import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def index2():
    return render_template('index-2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = shelve.open('storage.db', 'r')
        users = db['Users']
        db.close()
        
        for key in users:
            if request.form['user-name'] == users[key].get_username() and request.form['user-password'] == users[key].get_password():
                print(f"User {users[key].get_username()} has logged in successfully!")
                return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = shelve.open('storage.db', 'c')
        try:
            users = db['Users']
        except:
            users = {}

        user = User.User(request.form['user-name'], request.form['user-password'], request.form['user-email'])
        users[user.get_user_id()] = user
        db['Users'] = users
        db.close()

        print(f"User created successfully! {user.get_username()} {user.get_password()} {user.get_email()}")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin/index.html')

if __name__ == '__main__':
    app.run(debug=True)