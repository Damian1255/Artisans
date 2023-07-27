import random
from classes import SupportTicket
from components import DbManager, ProductManager

db = DbManager.DbManager()

class SupportManager():
    def new_ticket(self, firstName, lastName, email, countryCode, phoneNumber, subject, message):
        ticket_list = db.get_support_ticket_list()

        ticket_id = random.randint(100000, 999999)
        while ticket_id in ticket_list:
            ticket_id = random.randint(100000, 999999)

        ticket = SupportTicket.SupportTicket(ticket_id, firstName, lastName, email, countryCode, phoneNumber, subject, message)
        ticket_list[ticket_id] = ticket

        db.update_support_ticket_list(ticket_list)
        print(f'Support Ticket #{ticket_id} created.')
        return True
    
    def get_ticket(self, ticket_id):
        ticket_list = db.get_support_ticket_list()
        if ticket_id in ticket_list:
            print(f'Support Ticket #{ticket_id} retrieved.')
            return ticket_list[ticket_id]
        else:
            print(f'Support Ticket #{ticket_id} not found.')
            return False
        
    def get_ticket_list(self):
        ticket_list = db.get_support_ticket_list()
        print(f'Support Tickets retrieved.')
        return ticket_list
    
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