import random, datetime
from classes import SupportTicket
from components import DbManager

db = DbManager.DbManager()

class SupportManager():
    # Creates a new support ticket
    def new_ticket(self, firstName, lastName, email, countryCode, phoneNumber, category, subject, message):
        ticket_list = db.get_support_ticket_list()

        ticket_id = random.randint(100000, 999999)
        while ticket_id in ticket_list:
            ticket_id = random.randint(100000, 999999)

        created_date = datetime.datetime.now().strftime("%Y-%m-%d")
        ticket = SupportTicket.SupportTicket(ticket_id, firstName, lastName, email, countryCode, phoneNumber, category, subject, message, created_date, 'Open')
        ticket_list[ticket_id] = ticket

        db.update_support_ticket_list(ticket_list)
        print(f'Support Ticket #{ticket_id} created.')
        return True
    
    # get ticket by id
    def get_ticket(self, ticket_id):
        ticket_list = db.get_support_ticket_list()
        if ticket_id in ticket_list:
            print(f'Support Ticket #{ticket_id} retrieved.')
            return ticket_list[ticket_id]
        else:
            print(f'Support Ticket #{ticket_id} not found.')
            return False
    
    # get all tickets
    def get_ticket_list(self):
        ticket_list = db.get_support_ticket_list()
        print(f'Support Tickets retrieved.')
        return ticket_list
    
    # delete ticket by id
    def delete_ticket(self, ticket_id):
        ticket_list = db.get_support_ticket_list()
        
        if ticket_id in ticket_list:
            del ticket_list[ticket_id]
            db.update_support_ticket_list(ticket_list)
            print(f'Support Ticket #{ticket_id} deleted.')
            return True
        else:
            print(f'Support Ticket #{ticket_id} not found.')
            return False
    
    # update ticket status
    def set_status(self, ticket_id, status):
        ticket_list = db.get_support_ticket_list()
        
        if ticket_id in ticket_list:
            ticket_list[ticket_id].set_status(status)
            db.update_support_ticket_list(ticket_list)
            print(f'Support Ticket #{ticket_id} status updated.')
            return True
        else:
            print(f'Support Ticket #{ticket_id} not found.')
            return False