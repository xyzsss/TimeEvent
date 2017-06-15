# coding:utf-8
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mike/github/TimeEvent/timeEvent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# DEVELOPMENT
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.secret_key = "sawadika"


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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref('events', lazy='dynamic'))

    def __init__(self, title, body, user, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.user = user

    def __repr__(self):
        return '<Event %r>' % self.title


if __name__ == "__main__":
    # db.drop_all()
    print 'db User droped!'
    db.create_all()
    print 'db User created!'
    admin = User(
        name='admin', email='admin@admin.com', password='123', extra="")
    guest = User(
        name='guest', email='guest@guest.com', password='123', extra="")
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    event1 = Event(
        title='test1',
        body="t1", user=User.query.filter_by(name='admin').first())
    event2 = Event(
        title='This was the second event',
        body="About sth ...", user=User.query.filter_by(name='admin').first())
    db.session.add(event1)
    db.session.add(event2)
    db.session.commit()
    print User.query.all()
    print Event.query.all()

"""
    from schema import db, User, Post
    db.create_all()
    admin = User(
        name='admin', email='admin@admin.com', password='123', extra="")
    db.session.add(admin)
    db.session.commint()
    User.query.all()
"""
