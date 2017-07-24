from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mike/github/TimeEvent/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class TUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    extra = db.Column(db.String(240))

    def __init__(self, name, email, password, extra):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.extra = extra

    def __repr__(self):
        return '<User %r>' % self.name


if __name__ == "__main__":
    # If imported
    # from password import db, TUser
    # Generate db file
    db.drop_all()
    db.create_all()

    print 'Query before insert!'
    print TUser.query.all()

    print 'Insert data'
    admin = TUser('admin', 'admin@xy.cn', 'ssss', 'ss')
    db.session.add(admin)
    db.session.commit()
    print TUser.query.all()

    # Verify password
    print 'Verify password:'
    print check_password_hash(TUser.query.all()[0].password_hash, 'ssss')
    # manager.run()
