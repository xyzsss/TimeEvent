from flask_wtf import FlaskForm
from wtforms import TextField,\
    TextAreaField, SubmitField, HiddenField, PasswordField
from wtforms import validators, ValidationError


WTF_CSRF_SECRET_KEY = 'a random string'


class UserForm(FlaskForm):
    name = TextField(
        "User Name",
        [validators.Required("Please enter your name")])
    password = PasswordField(
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
    is_update = HiddenField('Is update', default=None)
    event_id = HiddenField(default=False)
    update_date = HiddenField(default=False)
    submit = SubmitField("Send")


class UpdatePassForm(FlaskForm):
    old_pass = PasswordField(
        "Current Password",
        [validators.Required("Please enter your current password")])
    new_pass = PasswordField(
        "New Password",
        [validators.Required("Please enter your new password")])
    new_pass_verify = PasswordField(
        "Verify New Password",
        [validators.Required("Please enter your new password Again")])
    submit = SubmitField("Update")
