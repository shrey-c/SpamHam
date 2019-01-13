from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError
from SponsCentral.models import User, PartyUser, SponsorUser, Conversing, Conversation

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Proceed')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class MailBoxText(FlaskForm):
    recepient = StringField('Enter Recepient', validators=[DataRequired(), Length(min=1, max=100),Email=()])
    mail = StringField('Enter Text', validators=[DataRequired(), Length(min=1, max=500)])
    send = SubmitField('Send')
