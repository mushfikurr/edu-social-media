from flask_wtf import FlaskForm
from lore.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


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


class UpdateAccountForm(FlaskForm):
    """
    Form used for updating account details
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
    submit = SubmitField('Update')

    # Custom Validation
    def validate_username(self, username):
        if username.data != current_user.username:
            query_user = User.query.filter_by(username=username.data).first()
            if query_user:
                print('failed username validation')
                raise ValidationError('That username is taken. Please try another one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            query_user = User.query.filter_by(username=email.data).first()
            if query_user:
                print('failed email validation')
                raise ValidationError('That email address is taken. Please try another one.')
    
