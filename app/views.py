from app import app

from app.forms import MentorRequestForm
from app.database import Database
from app.auth import requires_auth

from flask import render_template

@app.route('/')
def index():
    return "hello world"

@app.route('/help', methods=['GET', 'POST'])
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

        return render_template('success.html')

    return render_template('help.html',
            title='Mentor me!',
            form=form)

@app.route('/admin')
@requires_auth
def admin_panel():
    tickets = Database.get_tickets('all')
    return render_template('tickets_admin.html',
            tickets=tickets)
