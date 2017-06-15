# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from forms import *
from flask_sqlalchemy import SQLAlchemy
from schema import User, Event, db
# DEVEPLOMENT
import pdb
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
Bootstrap(app)

# ENABLE DEBUG TOOLBAR
app.debug = True
app.config['SECRET_KEY'] = 'development'
# SQL detail
# app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# development changed
app.secret_key = "sawadika"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://scott:tiger@127.0.0.1/mydatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mike/github/TimeEvent/timeEvent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

# development added
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


def get_elapsed_time(time_before):
    if time_before:
        time_now = datetime.utcnow()
        ela_sec = int((time_now - time_before).total_seconds())
        hour_num = ela_sec / 60
        if hour_num == 0:
            elapsed_time = "less in one minutes"
        elif hour_num < 60:
            elapsed_time = str(hour_num) + " minutes before"
        elif hour_num >= 60 and hour_num < 3600:
            elapsed_time = str(hour_num / 60) + " hours before"
        elif hour_num >= 3600:
            elapsed_time = str(hour_num / 3600) + " days before"
    else:
        elapsed_time = 'unknow'
    return elapsed_time


def get_event_by_user(events):
    rows = []
    for event in events:
        row = {
            'id': event.id,
            'title': event.title,
            'body': '.......',
            'pub_date': get_elapsed_time(event.pub_date),
            'user': str(event.user)}
        rows.append(row)
    return rows


@app.route('/events/<id>')
def events_detail(id):
    evt_obj = Event.query.get(id)
    title, body = evt_obj.title, evt_obj.body
    content = {
        'title': title,
        'body': body
    }
    return render_template('event_detail.html', content=content)


def split_page(records_all, the_order=1, every_page_num=15):
    total_events = len(records_all)
    if total_events % every_page_num != 0:
        total_page = total_events / every_page_num + 1
    else:
        total_page = total_events / every_page_num
    if the_order <= total_page and the_order > 0:
        records = records_all[(the_order - 1) * every_page_num:the_order * every_page_num]
    else:
        records = False
    return (total_page, records)


@app.route('/events/list/<page_num>')
def events_show(page_num):
    page_num = int(page_num)
    if 'username' in session:
        name = User.query.filter_by(name=session['username']).first()
        all_events = Event.query.order_by(Event.id.desc()).filter_by(user=name).all()
        total_page, events = split_page(all_events, the_order=page_num)
        rows = get_event_by_user(events)
        next_page = page_num + 1 if page_num + 1 <= total_page else False
        last_page = page_num - 1 if page_num > 1 else False
        return render_template(
            'show_event.html', events=rows, cur_page=page_num,
            total_page=total_page, next_page=next_page, last_page=last_page)
    message = "You come to place named No Man's Land "
    flash(message)
    return redirect(url_for('index'))


def insert_event_record(request, form):
    try:
        event_info = Event(
            title=request.form['title'],
            body=request.form['body'],
            user=User.query.filter_by(name=session['username']).first())
        db.session.add(event_info)
        db.session.commit()
        msg = "Record successfully added"
    except:
        msg = "error in insert operation"
        return render_template('events_add.html', form=form)
    finally:
        flash(msg)
        return redirect(url_for('events_show', page_num=1))


@app.route('/events/add', methods=['POST', 'GET'])
def events_add():
    form = EventForm()
    if request.method == 'POST':
        if form.validate() is False:
            flash("All fields are required.")
            return render_template('events_add.html', form=form)
        else:
            return insert_event_record(request, form)
    else:
        if 'username' in session:
            return render_template('events_add.html', form=form)
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
        return render_template('register.html', form=form)
    finally:
        flash(msg)
        return redirect(url_for('index'))


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('register.html', form=form, is_GET=True)
        else:
            return insert_user_record(request, form)
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/users/list')
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
        return redirect(url_for('user_login'))


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


@app.route('/user/login', )
def user_login():
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
    return redirect(url_for('user_login'))


@app.route('/user/logout')
def logout_action():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect(url_for('user_login'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
