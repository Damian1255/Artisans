from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import logging

from blueprints.admin import admin_blueprint
from blueprints.account import account_blueprint
from blueprints.db import db_blueprint


app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('configuration/config.py')

app.register_blueprint(admin_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(db_blueprint)

# disables flask logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.route('/')
def index():
    return render_template('artisan/index.html')

@app.route('/2')
def index2():
    return render_template('artisan/index-2.html')

@app.route('/about')
def about():
    return render_template('artisan/about.html')

@app.route('/customer-support')
def customer_support():
    return render_template('artisan/customer-support.html')

if __name__ == '__main__':
    app.run(debug=True)

