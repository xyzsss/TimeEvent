# coding:utf-8
from flask import Flask, render_template, request,\
    redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from forms import *
from flask_sqlalchemy import SQLAlchemy
from schema import User, Event, db
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import os


app = Flask(__name__)
Bootstrap(app)


# ********************** DEBUG **********************
# basic
app.config['SECRET_KEY'] = '<replace with a secret key>'

# debug
app.config['DEBUG'] = True
toolbar = DebugToolbarExtension(app)

# dev
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


# SQL
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db_default_path = 'sqlite:////data/github/TimeEvent/sqlite.db'
db_env_config = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_default_path if db_env_config is None else db_env_config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

SQLAlchemy(app)

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
    event_obj = Event.query.get(id)
    # convert to utc +8
    UTC_OFFSET = 8
    pub_date_local = event_obj.pub_date + timedelta(hours=UTC_OFFSET)
    pub_date_string = pub_date_local.strftime('%m/%d/%Y - %H:%M:%S')
    content = {
        'title': event_obj.title,
        'body': event_obj.body,
        'pub_date': pub_date_string
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


@app.route("/")
def index():
    if 'username' in session:
        name = session['username']
        return redirect(url_for('events_list', page_num=1))
    else:
        return redirect(url_for('user_login'))


@app.route('/events/list/<page_num>')
def events_list(page_num):
    page_num = int(page_num)
    if 'username' in session:
        name = User.query.filter_by(name=session['username']).first()
        all_events = Event.query.order_by(Event.id.desc()).filter_by(user=name).all()
        if all_events:
            total_page, events = split_page(all_events, the_order=page_num)
            rows = get_event_by_user(events)
            next_page = page_num + 1 if page_num + 1 <= total_page else False
            last_page = page_num - 1 if page_num > 1 else False
            return render_template(
                'events_list.html', events=rows, cur_page=page_num,
                total_page=total_page, name=session['username'],
                next_page=next_page, last_page=last_page)
        else:
            return render_template('events_list.html', noevents=True)
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
        return redirect(url_for('events_list', page_num=1))


def update_event_record(request, form):
    try:
        event_id = request.form['event_id']
        event_obj = Event.query.filter_by(id=event_id).first()
        event_obj.title, event_obj.body = request.form['title'], request.form['body']
        db.session.commit()
        msg = "Record successfully Updated"
    except:
        msg = "error in update operation"
        return render_template('events_mod.html', form=form)
    finally:
        flash(msg)
        return redirect(url_for('events_list', page_num=1))


@app.route('/events/add', methods=['POST', 'GET'])
def events_add():
    form = EventForm()
    if request.method == 'POST':
        if form.validate() is False:
            flash("All fields are required.")
            return render_template('events_add.html', form=form)
        else:
            if request.form['is_update']:
                return update_event_record(request, form)
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


@app.route('/events/modify/<event_id>', methods=['POST', 'GET'])
def event_mod(event_id):
    event_obj = Event.query.filter_by(id=event_id).first()
    user_obj = User.query.filter_by(name=session['username']).first()
    if event_obj is not None and user_obj.id is event_obj.user_id:
        eventForm = EventForm(
            event_id=event_obj.id,
            is_update=True,
            update_date=datetime.utcnow())
        event = {
            'title': event_obj.title,
            'body': event_obj.body,
            'is_update': True,
            'pub_date': event_obj.pub_date}
        return render_template('events_mod.html', form=eventForm, event=event)
    else:
        return render_template('404.html'), 404


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


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    form = UserForm(request.form)
    if request.method == 'POST' and not form.validate_on_submit():
        user_val = request.form['name']
        pass_val = request.form['password']
        if user_val and user_val is not '':
            user_obj = User.query.filter_by(name=user_val).first()
            if user_obj is not None:
                if check_password_hash(user_obj.password_hash, pass_val):
                    session['username'] = user_val
                    message = "Login Successful!"
                    flash(message)
                    return redirect(url_for('index'))
                else:
                    message = "Password input wrong!"
            else:
                message = "User '" + user_val + "' not exists!"
        else:
            message = "User empty not allowed!"
        flash(message)
    return render_template('login.html', form=form)


@app.route('/user/logout')
def logout_action():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect(url_for('user_login'))


@app.route('/user/chpasswd', methods=['POST', 'GET'])
def user_password_update():
    form = UpdatePassForm()
    if request.method == 'POST' and form.validate_on_submit():
        old_pass = request.form['old_pass']
        new_pass = request.form['new_pass']
        user_obj = User.query.filter_by(name=session['username']).first()
        if new_pass == request.form['new_pass_verify']\
                and check_password_hash(user_obj.password_hash, old_pass):
            user_obj.password_hash = generate_password_hash(new_pass)
            db.session.commit()
            message = "Updated successful!"
        else:
            message = "New password not matched!"
        flash(message)
        return render_template('chpasswd.html', form=form)
    return render_template('chpasswd.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
