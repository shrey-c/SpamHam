from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError
from SH.models import User, Emails , Conversation

class RegisterForm(FlaskForm):
    email_id = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Proceed')

    def validate_email(self, email_id):
        user = User.query.filter_by(email_id=email_id.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email_id = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class MailBoxText(FlaskForm):
    email_id = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    text = StringField('Enter Text', validators=[DataRequired(), Length(min=1, max=500)])
    send = SubmitField('Send')

    def validate_email(self, email_id):
        user = User.query.filter_by(email_id=email_id.data).first()
        if user == None:
            raise ValidationError('No such email')
