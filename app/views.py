from app import app

from app.forms import MentorRequestForm
from app.database import Database
from app.auth import requires_auth

from flask import render_template, request

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def mentor_request():
    form = MentorRequestForm()
    if form.validate_on_submit():
        try:
            user_id = Database.create_user_if_not_exists(
                    form.user_name.data,
                    form.user_email.data)
        except ValueError as e:
            return render_template('message.html', message=str(e))

        try:
            ticket_id = Database.create_ticket(
                    user_id,
                    form.ticket_table_number.data,
                    form.ticket_contents.data,
                    'pending')
        except ValueError as e:
            return "database is totally borked"

        return render_template('chat.html', token=ticket['ticketId'])

    return render_template('help.html',
            title='Mentor me!',
            form=form)

@app.route('/admin', defaults={'ticket_status': 'all'})
@app.route('/admin/<ticket_status>')
@requires_auth
def admin_panel(ticket_status):
    try:
        tickets = Database.list_tickets(ticket_status)
    except ValueError:
        return render_template('message.html', message=str(e))

    ticket_statuses = Database.get_ticket_status_names()
    return render_template('tickets_admin.html',
            tickets=tickets,
            ticket_statuses=ticket_statuses,
            password=app.config['ADMIN_MESSAGE_PASSWORD'],
            angular_app='ticketApp')
