from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    """
    Form used for Register page.
    """
    # Validators
    name_validator = [DataRequired(), Length(max=256)]
    # All fields
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=16)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    first_name = StringField(
        'Forename',
        validators=name_validator
    )
    last_name = StringField(
        'Surname',
        validators=name_validator
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    Form used for Login page.
    """
    # All fields
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=16)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember = BooleanField(
        'Remember Me'
    )
    submit = SubmitField('Login')
