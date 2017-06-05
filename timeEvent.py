# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from forms import UserForm
from flask_sqlalchemy import SQLAlchemy
from schema import *

app = Flask(__name__)
Bootstrap(app)

# development changed
app.secret_key = "sawadika"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mike/github/TimeEvent/timeEvent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# development added
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


def get_event_by_user(events):
    rows = []
    for event in events:
        row = {
            'title': event.title,
            'body': '~~~~~',
            'pub_date': event.pub_date,
            'user': str(event.user)}
        rows.append(row)
    return rows


@app.route('/<user>/events')
def show_event(user):
    if 'username' in session:
        if session['username'] == user:
            name = User.query.filter_by(name=session['username']).first()
            events = Event.query.filter_by(user=name).all()
            rows = get_event_by_user(events)
            return render_template('show_event.html', events=rows)
        else:
            message = "You come to place named No Man's Land "
    flash(message)
    return redirect(url_for('index'))


def insert_user_record(request, form):
    try:
        user_info = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            extra=request.form['extra'])
        db.session.add(user_info)
        db.session.commit()
        msg = "Record successfully added"
    except:
        msg = "error in insert operation"
    finally:
        flash(msg)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('register.html', form=form, is_GET=True)
        else:
            return insert_user_record(request, form)
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/userList')
def list_users():
    user_list = User.query.all()
    rows = []
    for user in user_list:
        row = {
            'name': user.name,
            'email': user.email,
            'extra': user.extra}
        rows.append(row)
    return render_template("users_list.html", Users=rows)


@app.route("/")
def index():
    if 'username' in session:
        name = session['username']
        return render_template('bt_demo.html', name=name)
    else:
        return redirect(url_for('login'))


@app.route("/time")
def get_curr_time():
    curr_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('show_page.html', curr_time=curr_time)


@app.route('/hello/<name>')
def hello_name(name):
    if name == 'mike':
        return redirect(url_for('get_curr_time'))
    else:
        return render_template('show_page.html', name=name)


@app.route('/login', )
def login():
    return render_template('login.html')


@app.route('/loginCheck', methods=['POST', 'GET'])
def login_action():
    if request.method == 'POST':
        user_input = request.form['username'].strip()
        if user_input is not '':
            res = User.query.filter_by(name=user_input).first()
            if res is not None:
                session['username'] = user_input
                return redirect(url_for('index'))
            else:
                message = "User '" + user_input + "' not exists!"
        else:
            message = "User empty not allowed!"
    flash(message)
    return redirect(url_for('login'))


@app.route('/logout')
def logout_action():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
