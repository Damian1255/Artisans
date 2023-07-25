from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from components import DbManager, UserManager, SupportManager

support_bp = Blueprint(name="support_bp", import_name=__name__, url_prefix="/support/")

db = DbManager.DbManager()
user_manager = UserManager.UserManager()
support_manager = SupportManager.SupportManager()


@support_bp.route('/')
def index():
    return render_template('artisan/customer-support.html')


@support_bp.route('/submit/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        countryCode = request.json['countryCode']
        phoneNumber = request.json['phoneNumber']
        subject = request.json['messageSubject']
        message = request.json['message']

        if support_manager.new_ticket(firstName, lastName, email, countryCode, phoneNumber, subject, message):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})