from flask import Flask, render_template, request, current_app, session, redirect, url_for
import os
from common.database import Database
from common.utils import Utils
from models.users import Users
from models.admins import Admin
from email_sender import email

app = Flask(__name__)
app.secret_key = os.urandom(64)
ADMIN = app.config.update(ADMIN=os.environ.get('ADMIN'))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/lineup')
def lineup():
    return render_template('lineup.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'register' in request.form:
        full_name = request.form['full_name']
        email = request.form['email']
        password = Utils.encrypt_pass(request.form['password'])
        tickets_amount = request.form['tickets_amount']
        mat, instrument, food, camp = 0, 0, 0, 0
        if request.form.get('mat'):
            mat = 1
        if request.form.get('instrument'):
            instrument = 1
        if request.form.get('food'):
            food = 1
        if request.form.get('camp'):
            camp = 1

        items = Users.toJson(full_name, email, password, tickets_amount, mat, instrument, food, camp)
        if not Users.register(email, items):
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה כבר רשום במערכת',
                                   url='register')
        else:
            return render_template('user/confirm_registration.html', name=full_name, email=email)

    else:
        return render_template("user/registration.html")


@app.route('/maps')
def maps():
    return render_template('map.html')


@app.route('/cancelRegister', methods=['POST', 'GET'])
def cancel_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if Database.find_one_by('participants', {"email": email}) is None:
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו קיים במערכת',
                                   url='cancel_register')
        if not Users.login_valid(email, password):
            return render_template('user/unsuccessful_register.html', message='סיסמא שגויה', url='cancel_register')
        Database.remove('participants', {"email": email})
        return render_template('user/confirm_cancelation.html')
    else:
        return render_template('user/cancel_registration.html')


@app.route('/editRegister/<string:email_>', methods=['GET', 'POST'])
def edit_register(email_):
    if request.method == 'POST' and 'edit' in request.form:
        user = Database.find_one_by('participants', {"email": email_})
        full_name = user['full_name']
        email = email_
        password = user['password']
        tickets_amount = request.form['tickets_amount']
        mat, instrument, food, camp = False, False, False, False
        if request.form.get('mat'):
            mat = request.form.get('mat')
        if request.form.get('instrument'):
            instrument = request.form.get('instrument')
        if request.form.get('food'):
            food = request.form.get('food')
        if request.form.get('camp'):
            camp = request.form.get('camp')
        items = Users.toJson(full_name, email, password, tickets_amount, mat, instrument, food, camp)
        Database.update('participants', {"email": email}, items)
        return render_template('user/confirm_editing.html', name=full_name, email=email)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if Database.find_one_by('participants', {"email": email}) is None:
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו קיים במערכת',
                                   url='edit_register', email_='$')
        if not Users.login_valid(email, password):
            return render_template('user/unsuccessful_register.html', message='סיסמא שגויה', url='edit_register',
                                   email_='$')
        user = Database.find_one_by('participants', {"email": email})
        return render_template('user/edit_registration.html', email_=email, user=user)
    else:
        return render_template('user/edit_registration.html', email_='$')


@app.route('/adminsEnter', methods=['GET', 'POST'])
def admins_enter():
    if request.method == 'POST' and 'login' in request.form:
        email = request.form['email']
        password = request.form['password']
        user = Database.find_one_by('admins', {"email": email})
        if email != current_app.config.get('ADMIN', ''):
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו שייך למנהל',
                                   url='admins_enter')
        elif user is None:
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו קיים במערכת',
                                   url='admins_enter')
        elif not Admin.login_valid(email, password):
            return render_template('user/unsuccessful_register.html', message="הסיסמא שהזנת שגויה",
                                   url='admins_enter')
        else:
            session['email'] = email
            tickets_amount = Admin.sum_tickets_amount('participants')
            equipment_amount = Admin.equipment_amount('participants')
            tickets_by_name = Admin.tickets_by_name('participants')
            return render_template('admin/admins_page.html', full_name=user['full_name'], tickets_amount=tickets_amount,
                                   equipment=equipment_amount, tickets_by_name=tickets_by_name)

    elif request.method == 'POST' and 'register' in request.form:
        full_name = request.form['full_name']
        email = request.form['email']
        password = Utils.encrypt_pass(request.form['password'])
        items = Admin.toJson(full_name, email, password)
        if email != current_app.config.get('ADMIN', ''):
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו שייך למנהל',
                                   url='admins_enter')
        elif not Admin.register(email, items):
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה כבר רשום במערכת',
                                   url='admins_enter')
        else:
            return render_template('admin/admins_login-register.html', name=full_name, email=email)

    elif request.method == 'POST' and 'erase' in request.form:
        email = request.form['email']
        password = request.form['password']
        if Database.find_one_by('admins', {"email": email}) is None:
            return render_template('user/unsuccessful_register.html', message='דואר אלקטרוני זה אינו קיים במערכת',
                                   url='admins_enter')
        if not Admin.login_valid(email, password):
            return render_template('user/unsuccessful_register.html', message='סיסמא שגויה', url='admins_enter')
        Database.remove('admins', {"email": email})
        return render_template('user/confirm_cancelation.html')
    else:
        return render_template('admin/admins_login-register.html')


@app.route('/logout')
def admin_logout():
    session['email'] = None
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
