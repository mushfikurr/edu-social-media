from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                ValidationError)
from lore.main.models import User


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

    # Custom Validation
    def validate_username(self, username):
        """
        A custom validation error.
        This validation is for when a username is taken.
        """
        query_user = User.query.filter_by(username=username.data).first()
        if query_user:
            raise ValidationError(
                'That username is taken. Please try another one.'
            )

    def validate_email(self, email):
        """
        A custom validation error.
        This validation is for when a email is taken.
        """
        query_email = User.query.filter_by(email=email.data).first()
        if query_email:
            raise ValidationError(
                'That username is taken. Please try another one.'
            )


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
    submit = SubmitField('LOGIN')
