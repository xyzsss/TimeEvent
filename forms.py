from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField,\
    TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError


class UserForm(FlaskForm):
    name = TextField(
        "User Name",
        [validators.Required("Please enter your name")])
    password = TextField(
        "Password",
        [validators.Required("Please enter your password")])
    email = TextField(
        "Email",
        [validators.Required("Please enter your email address."),
         validators.Email("Please check your email format.")])
    extra = TextAreaField("Extra Info")
    submit = SubmitField("Send")


class EventForm(FlaskForm):
    title = TextField(
        "Eent Title",
        [validators.Required("Please enter your Event Title")])
    body = TextAreaField(
        "Event Detail",
        [validators.Required("Please enter your Event Content")])
    pub_date = TextField(
        "Publish Date")
    submit = SubmitField("Send")
