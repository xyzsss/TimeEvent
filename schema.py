# coding:utf-8
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mike/github/TimeEvent/timeEvent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = "sawadika"

# development added
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    extra = db.Column(db.String(240))

    def __init__(self, name, email, password, extra):
        self.name = name
        self.email = email
        self.password = password
        self.extra = extra

    def __repr__(self):
        return '<User %r>' % self.name


if __name__ == "__main__":
    db.drop_all()
    print 'db User droped!'
    db.create_all()
    print 'db User created!'
    admin = User(name='admin', email='admin@admin.com', password='123', extra="")
    guest = User(name='guest', email='guest@guest.com', password='123', extra="")
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    print User.query.all()

"""
    from db import db
    db.create_all()
    from db import User
    admin = User(
        name='admin', email='admin@admin.com', password='123', extra="")
    db.session.add(admin)
    db.session.commint()
    User.query.all()
"""
