from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from components import UserManager
import logging

from blueprints.admin import admin_blueprint
from blueprints.account import account_blueprint
from blueprints.db import db_blueprint

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nani'

app.register_blueprint(admin_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(db_blueprint)

# disables flask logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

user_manager = UserManager.UserManager('storage/storage.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def index2():
    return render_template('index-2.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
