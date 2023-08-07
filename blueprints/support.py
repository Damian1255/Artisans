from datetime import datetime
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
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
        category = request.json['category']
        subject = request.json['messageSubject']
        message = request.json['message']

        if support_manager.new_ticket(firstName, lastName, email, countryCode, phoneNumber, category, subject, message):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        
@support_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        ticket_id = request.json['ticket_id']

        if support_manager.delete_ticket(ticket_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        

@support_bp.route('/status/update', methods=['GET', 'POST'])
def status_update():
    if request.method == 'POST':
        ticket_id = request.json['ticket_id']
        status = request.json['status']

        if support_manager.set_status(ticket_id, status):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        

@support_bp.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        records = []
        close = 0

        tickets = support_manager.get_ticket_list()
        for ticket in tickets:
            date = tickets[ticket].get_date_created()
            id = tickets[ticket].get_ticket_id()
            customer = tickets[ticket].get_first_name() + ' ' + tickets[ticket].get_last_name()
            category = tickets[ticket].get_category()
            subject = tickets[ticket].get_subject()
            status = tickets[ticket].get_status()

            records.append({
                'date': date,
                'customer': customer,
                'category': category,
                'subject': subject,
                'status': status,
                'count': 1
            })

            if status == 'Closed':
                close += 1

        # check for empty gap in date to fill with 0
        try:
            start_date = datetime.strptime(records[0]['date'], '%Y-%m-%d').date()
        except:
            start_date = datetime.today().date()
        end_date = datetime.today().date()

        for date in pd.date_range(start_date, end_date):
            date = date.strftime('%Y-%m-%d')
            if not any(record['date'] == date for record in records):
                records.append({
                    'date': date, 'customer': '', 'category': '',
                    'subject': '', 'status': '', 'count': 0
                })

        df = pd.DataFrame(records).groupby(['date']).sum(numeric_only=True).reset_index()
        tickets = df.to_dict('list')

        df = pd.DataFrame(records).groupby(['category']).sum(numeric_only=True).reset_index()
        df.sort_values(by=['count'], inplace=True, ascending=False)
        tickets_category = df.to_dict('list')

        return jsonify({
            'tickets': tickets,
            'tickets_category': tickets_category,
            'tickets_total': [len(tickets), close]
        })