# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from forms import UserForm
import sqlite3 as sql


app = Flask(__name__)
Bootstrap(app)

# development changed
app.secret_key = "sawadika"
DATABASE = 'timeEvent.db'

# development added
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


def insert_user_record(request, form):
    try:
        u_name, u_email, u_password, u_extra = (
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['extra']
        )
        with sql.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Users (name, email, password, extra) VALUES (?,?,?,?)", (u_name, u_email, u_password, u_extra)
            )
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        flash(msg)
        con.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        print request.form["csrf_token"]
        if form.validate() is False:
            return render_template('register.html', form=form, is_GET=True)
        else:
            return insert_user_record(request, form)
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/userList')
def list_users():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select name, email, extra from Users")
    rows = cur.fetchall()
    for row in rows:
        print row
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
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/logout')
def logout_action():
    session.pop('username', None)
    flash('You were successfully logged out!')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
