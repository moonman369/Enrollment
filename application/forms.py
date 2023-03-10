from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=15)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=55)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=55)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=15)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=15), EqualTo('password')])
    submit = SubmitField('Register Now')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use. Choose a different email and try again.')

    