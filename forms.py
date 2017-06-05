from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField,\
    TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError


class UserForm(FlaskForm):
    name = TextField(
        "User name",
        [validators.Required("Please enter your name")])
    password = TextField(
        "Password",
        [validators.Required("Please enter your password")])
    email = TextField(
        "Email",
        [validators.Required("Please enter your email address."),
         validators.Email("Please check your email format.")])
    extra = TextAreaField("Extra info")
    submit = SubmitField("Send")
